import { useState, useEffect } from 'react';

export interface AddOnOption {
  id: number;
  name: string;
  description: string;
  price: number;
  is_default: boolean;
  order: number;
}

export interface AddOn {
  id: number;
  name: string;
  slug: string;
  addon_type: 'single' | 'multiple' | 'checkbox';
  description: string;
  short_description: string;
  base_price: number;
  pricing_type: 'fixed' | 'per_person' | 'per_group' | 'percentage';
  currency: string;
  is_required: boolean;
  is_default: boolean;
  max_quantity: number;
  image?: string;
  features: string[];
  options: AddOnOption[];
  calculated_price: number;
}

export interface AddOnCategory {
  id: number;
  name: string;
  slug: string;
  category_type: string;
  description: string;
  icon: string;
  addons: AddOn[];
}

export interface SelectedAddOn {
  addon_id: number;
  option_id?: number;
  quantity: number;
  unit_price: number;
  total_price: number;
  name: string;
}

export interface BookingCalculation {
  base_total: number;
  addon_total: number;
  grand_total: number;
  currency: string;
  breakdown: {
    ticket: {
      name: string;
      unit_price: number;
      quantity: number;
      total: number;
    };
    addons: Array<{
      addon_id: number;
      option_id?: number;
      name: string;
      unit_price: number;
      quantity: number;
      total_price: number;
      pricing_type: string;
    }>;
  };
}

export const useAddOns = (ticketId?: number, travelers: number = 1) => {
  const [categories, setCategories] = useState<AddOnCategory[]>([]);
  const [selectedAddOns, setSelectedAddOns] = useState<SelectedAddOn[]>([]);
  const [selectedOptions, setSelectedOptions] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load add-ons for a specific ticket
  const loadAddOns = async (ticketId: number, travelers: number = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/tickets/${ticketId}/addons/?travelers=${travelers}`
      );
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.error || `Failed to load add-ons (${response.status})`;
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      
      if (data.success) {
        setCategories(data.categories);
        
        // Set default selections for required add-ons
        const defaultOptions: { [key: string]: string } = {};
        const defaultAddOns: SelectedAddOn[] = [];
        
        data.categories.forEach((category: AddOnCategory) => {
          category.addons.forEach((addon: AddOn) => {
            if (addon.is_required && addon.addon_type === 'multiple') {
              // Find default option
              const defaultOption = addon.options.find(opt => opt.is_default);
              if (defaultOption) {
                defaultOptions[addon.slug] = defaultOption.id.toString();
                
                // Add to selected add-ons if it has a price
                if (defaultOption.price > 0) {
                  defaultAddOns.push({
                    addon_id: addon.id,
                    option_id: defaultOption.id,
                    quantity: 1,
                    unit_price: defaultOption.price,
                    total_price: defaultOption.price,
                    name: `${addon.name} - ${defaultOption.name}`
                  });
                }
              }
            } else if (addon.is_default && addon.addon_type === 'checkbox') {
              // Auto-select default checkbox add-ons
              defaultAddOns.push({
                addon_id: addon.id,
                quantity: 1,
                unit_price: addon.calculated_price,
                total_price: addon.calculated_price,
                name: addon.name
              });
            }
          });
        });
        
        setSelectedOptions(defaultOptions);
        setSelectedAddOns(defaultAddOns);
      } else {
        throw new Error(data.error || 'Failed to load add-ons');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error loading add-ons:', err);
    } finally {
      setLoading(false);
    }
  };

  // Calculate total booking cost
  const calculateTotal = async (ticketId: number, quantity: number, travelers: number) => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/tickets/calculate-total/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ticket_id: ticketId,
            quantity,
            travelers,
            selected_addons: selectedAddOns.map(addon => ({
              addon_id: addon.addon_id,
              option_id: addon.option_id,
              quantity: addon.quantity
            }))
          })
        }
      );

      if (!response.ok) {
        throw new Error('Failed to calculate total');
      }

      const data = await response.json();
      
      if (data.success) {
        return data.calculation as BookingCalculation;
      } else {
        throw new Error(data.error || 'Failed to calculate total');
      }
    } catch (err) {
      console.error('Error calculating total:', err);
      throw err;
    }
  };

  // Handle option selection for multiple-choice add-ons
  const handleOptionChange = (addonSlug: string, optionId: string, addon: AddOn) => {
    setSelectedOptions(prev => ({
      ...prev,
      [addonSlug]: optionId
    }));

    // Update selected add-ons
    const option = addon.options.find(opt => opt.id.toString() === optionId);
    if (option) {
      setSelectedAddOns(prev => {
        // Remove existing selection for this add-on
        const filtered = prev.filter(item => item.addon_id !== addon.id);
        
        // Add new selection if it has a price
        if (option.price > 0) {
          filtered.push({
            addon_id: addon.id,
            option_id: option.id,
            quantity: 1,
            unit_price: option.price,
            total_price: option.price,
            name: `${addon.name} - ${option.name}`
          });
        }
        
        return filtered;
      });
    }
  };

  // Handle checkbox add-on toggle
  const handleAddOnToggle = (addon: AddOn, selected: boolean) => {
    if (selected) {
      // Add to selected add-ons
      setSelectedAddOns(prev => [
        ...prev.filter(item => item.addon_id !== addon.id),
        {
          addon_id: addon.id,
          quantity: 1,
          unit_price: addon.calculated_price,
          total_price: addon.calculated_price,
          name: addon.name
        }
      ]);
    } else {
      // Remove from selected add-ons
      setSelectedAddOns(prev => prev.filter(item => item.addon_id !== addon.id));
    }
  };

  // Check if an add-on is selected
  const isAddOnSelected = (addonId: number) => {
    return selectedAddOns.some(item => item.addon_id === addonId);
  };

  // Get selected option for a multiple-choice add-on
  const getSelectedOption = (addonSlug: string) => {
    return selectedOptions[addonSlug];
  };

  // Load add-ons when ticketId changes
  useEffect(() => {
    if (ticketId && ticketId > 0) {
      loadAddOns(ticketId, travelers);
    }
  }, [ticketId, travelers]);

  return {
    categories,
    selectedAddOns,
    selectedOptions,
    loading,
    error,
    loadAddOns,
    calculateTotal,
    handleOptionChange,
    handleAddOnToggle,
    isAddOnSelected,
    getSelectedOption,
    setSelectedAddOns
  };
};