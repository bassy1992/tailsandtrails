import { useState, useEffect } from 'react';
import { validateId, shouldMakeApiCall, getErrorMessage, getPathType } from '../utils/idValidation';

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

export const useAddOns = (id?: number, travelers: number = 1, itemType: 'destination' | 'ticket' = 'destination') => {
  const [categories, setCategories] = useState<AddOnCategory[]>([]);
  const [selectedAddOns, setSelectedAddOns] = useState<SelectedAddOn[]>([]);
  const [selectedOptions, setSelectedOptions] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load add-ons for a specific item (destination or ticket)
  const loadAddOns = async (id: number, travelers: number = 1) => {
    // Comprehensive ID validation
    if (!shouldMakeApiCall(id, itemType)) {
      const errorMessage = getErrorMessage(id, itemType);
      console.warn(`🚫 Preventing API call for invalid ${itemType} ID ${id}`);
      setError(errorMessage);
      setCategories([]);
      setSelectedAddOns([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      let endpoint: string;
      let transformData: (data: any) => any;

      if (itemType === 'destination') {
        // For destinations, get add-ons from the destination detail endpoint
        endpoint = `destinations/${id}/`;
        transformData = (data: any) => {
          // Transform destination add-ons to match the expected format
          const categories: AddOnCategory[] = [];
          
          // Group addon_options by category
          const categoryMap = new Map();
          
          if (data.addon_options && data.addon_options.length > 0) {
            data.addon_options.forEach((option: any) => {
              // Determine category based on option name since backend categories are empty
              let categoryName = 'general';
              let categoryDisplayName = 'General Options';
              let categoryIcon = 'star';
              
              const optionName = option.name.toLowerCase();
              if (optionName.includes('hotel') || optionName.includes('resort') || optionName.includes('accommodation') || optionName.includes('lodge') || optionName.includes('room')) {
                categoryName = 'accommodation';
                categoryDisplayName = 'Accommodation Options';
                categoryIcon = 'hotel';
              } else if (optionName.includes('bus') || optionName.includes('car') || optionName.includes('transport') || optionName.includes('vehicle') || optionName.includes('taxi') || optionName.includes('shuttle')) {
                categoryName = 'transport';
                categoryDisplayName = 'Transport Options';
                categoryIcon = 'car';
              } else if (optionName.includes('meal') || optionName.includes('food') || optionName.includes('dining') || optionName.includes('lunch') || optionName.includes('dinner') || optionName.includes('breakfast')) {
                categoryName = 'meals';
                categoryDisplayName = 'Meal Options';
                categoryIcon = 'utensils';
              } else if (optionName.includes('insurance') || optionName.includes('medical') || optionName.includes('health') || optionName.includes('safety') || optionName.includes('coverage')) {
                categoryName = 'medical';
                categoryDisplayName = 'Medical & Insurance';
                categoryIcon = 'shield';
              }
              
              if (!categoryMap.has(categoryName)) {
                const categoryDescriptions = {
                  accommodation: 'Choose your preferred accommodation level',
                  transport: 'Select your transportation preferences', 
                  meals: 'Customize your dining experience',
                  medical: 'Health and safety coverage options',
                  general: 'Additional options for your experience'
                };
                
                const categoryIds = {
                  accommodation: 1,
                  transport: 2,
                  meals: 3,
                  medical: 4,
                  general: 5
                };
                
                categoryMap.set(categoryName, {
                  id: categoryIds[categoryName as keyof typeof categoryIds] || 5,
                  name: categoryDisplayName,
                  slug: categoryName,
                  category_type: categoryName,
                  description: categoryDescriptions[categoryName as keyof typeof categoryDescriptions] || 'Additional options',
                  icon: categoryIcon,
                  addons: []
                });
              }
              
              // Transform option to addon format
              const addon = {
                id: option.id,
                name: option.name,
                slug: `${categoryName}-${option.id}`,
                addon_type: 'multiple' as const,
                description: option.description,
                short_description: option.description,
                base_price: Number(option.price),
                pricing_type: option.pricing_type,
                currency: 'GHS',
                is_required: false,
                is_default: option.is_default,
                max_quantity: 1,
                features: [],
                options: [{
                  id: option.id,
                  name: option.name,
                  description: option.description,
                  price: Number(option.price),
                  is_default: option.is_default,
                  order: option.order
                }],
                calculated_price: Number(option.price)
              };
              
              categoryMap.get(categoryName).addons.push(addon);
            });
          }
          
          // Add experience add-ons as a separate category
          if (data.experience_addons && data.experience_addons.length > 0) {
            const experienceCategory = {
              id: 999,
              name: 'Additional Experiences',
              slug: 'experience',
              category_type: 'experience',
              description: 'Enhance your tour with extra activities',
              icon: 'camera',
              addons: data.experience_addons.map((exp: any) => ({
                id: exp.id + 1000, // Offset to avoid ID conflicts
                name: exp.name,
                slug: `experience-${exp.id}`,
                addon_type: 'checkbox' as const,
                description: exp.description,
                short_description: exp.description,
                base_price: Number(exp.price),
                pricing_type: 'per_person',
                currency: 'GHS',
                is_required: false,
                is_default: false,
                max_quantity: 1,
                features: exp.duration ? [`Duration: ${exp.duration}`] : [],
                options: [],
                calculated_price: Number(exp.price)
              }))
            };
            categoryMap.set('experience', experienceCategory);
          }
          
          return {
            success: true,
            categories: Array.from(categoryMap.values())
          };
        };
      } else {
        // For tickets, use the existing add-ons endpoint
        endpoint = `tickets/${id}/addons/?travelers=${travelers}`;
        transformData = (data: any) => data;
      }
      
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/${endpoint}`
      );
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.error || `Failed to load add-ons (${response.status})`;
        throw new Error(errorMessage);
      }
      
      const rawData = await response.json();
      const data = transformData(rawData);
      
      if (data.success || (itemType === 'destination' && data.categories)) {
        const categories = data.categories || [];
        setCategories(categories);
        
        // Set default selections for required add-ons
        const defaultOptions: { [key: string]: string } = {};
        const defaultAddOns: SelectedAddOn[] = [];
        
        categories.forEach((category: AddOnCategory) => {
          console.log(`📋 Processing category: ${category.name}`);
          category.addons.forEach((addon: AddOn) => {
            console.log(`🎯 Processing add-on: ${addon.name} (ID: ${addon.id}, type: ${addon.addon_type}, is_default: ${addon.is_default})`);
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
                    unit_price: Number(defaultOption.price),
                    total_price: Number(defaultOption.price),
                    name: `${addon.name} - ${defaultOption.name}`
                  });
                }
              }
            } else if (addon.is_default && addon.addon_type === 'checkbox') {
              // Auto-select default checkbox add-ons
              console.log(`🔄 Auto-selecting default checkbox add-on: ${addon.name} (ID: ${addon.id})`);
              defaultAddOns.push({
                addon_id: addon.id,
                quantity: 1,
                unit_price: Number(addon.calculated_price),
                total_price: Number(addon.calculated_price),
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
  const calculateTotal = async (id: number, quantity: number, travelers: number) => {
    try {
      const endpoint = itemType === 'destination' 
        ? 'destinations/calculate-total/'
        : 'tickets/calculate-total/';
      
      const bodyKey = itemType === 'destination' ? 'destination_id' : 'ticket_id';
      
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/${endpoint}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            [bodyKey]: id,
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
    setSelectedAddOns(prev => {
      // Remove existing selection for this add-on
      const filtered = prev.filter(item => item.addon_id !== addon.id);
      
      // If optionId is empty, user selected "Skip this option"
      if (!optionId) {
        return filtered; // Just remove, don't add anything
      }
      
      // Find the selected option
      const option = addon.options.find(opt => opt.id.toString() === optionId);
      if (option) {
        // Add new selection if it has a price
        if (option.price > 0) {
          filtered.push({
            addon_id: addon.id,
            option_id: option.id,
            quantity: 1,
            unit_price: Number(option.price),
            total_price: Number(option.price),
            name: `${addon.name} - ${option.name}`
          });
        }
      }
      
      return filtered;
    });
  };

  // Handle checkbox add-on toggle
  const handleAddOnToggle = (addon: AddOn, selected: boolean) => {
    console.log(`🔄 Toggle add-on: ${addon.name}, selected: ${selected}`);
    
    if (selected) {
      // Add to selected add-ons
      setSelectedAddOns(prev => {
        const filtered = prev.filter(item => item.addon_id !== addon.id);
        const newSelection = {
          addon_id: addon.id,
          quantity: 1,
          unit_price: Number(addon.calculated_price),
          total_price: Number(addon.calculated_price),
          name: addon.name
        };
        console.log(`➕ Adding add-on:`, newSelection);
        return [...filtered, newSelection];
      });
    } else {
      // Remove from selected add-ons
      setSelectedAddOns(prev => {
        const filtered = prev.filter(item => item.addon_id !== addon.id);
        console.log(`➖ Removing add-on: ${addon.name}`);
        return filtered;
      });
    }
  };

  // Check if an add-on is selected
  const isAddOnSelected = (addonId: number) => {
    const isSelected = selectedAddOns.some(item => item.addon_id === addonId);
    console.log(`🔍 Checking if add-on ${addonId} is selected:`, isSelected, 'Current selections:', selectedAddOns.map(s => s.addon_id));
    return isSelected;
  };

  // Get selected option for a multiple-choice add-on
  const getSelectedOption = (addonSlug: string) => {
    return selectedOptions[addonSlug];
  };

  // Load add-ons when ID changes
  useEffect(() => {
    if (id && id > 0) {
      // Comprehensive ID validation
      const validation = validateId(id, itemType);
      if (validation.isValid) {
        loadAddOns(id, travelers);
      } else {
        console.warn(`🚫 Invalid ${itemType} ID ${id}, not loading add-ons`);
        setError(validation.errorMessage || `Invalid ${itemType} ID`);
        setCategories([]);
        setSelectedAddOns([]);
        setLoading(false);
      }
    } else {
      // Clear state if no valid ID
      setCategories([]);
      setSelectedAddOns([]);
      setError(null);
      setLoading(false);
    }
  }, [id, travelers, itemType]);

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