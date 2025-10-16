import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { Loader2, Hotel, Car, Utensils, Shield, Star } from 'lucide-react';
import { useAddOns, AddOnCategory, AddOn } from '@/hooks/useAddOns';

interface AddOnSelectorProps {
  ticketId: number;
  travelers?: number;
  onSelectionChange?: (selectedAddOns: any[], totalAddonPrice: number) => void;
  className?: string;
  itemType?: 'destination' | 'ticket';
}

const getIconComponent = (iconName: string) => {
  const icons: { [key: string]: React.ComponentType<any> } = {
    Hotel,
    Car,
    Utensils,
    Shield,
    Star
  };
  
  return icons[iconName] || Star;
};

const AddOnSelector: React.FC<AddOnSelectorProps> = ({
  ticketId,
  travelers = 1,
  onSelectionChange,
  className = '',
  itemType = 'ticket'
}) => {
  const {
    categories,
    selectedAddOns,
    selectedOptions,
    loading,
    error,
    handleOptionChange,
    handleAddOnToggle,
    isAddOnSelected,
    getSelectedOption
  } = useAddOns(ticketId, travelers, itemType);

  // Notify parent component of selection changes
  React.useEffect(() => {
    if (onSelectionChange) {
      const totalAddonPrice = selectedAddOns.reduce((sum, addon) => sum + addon.total_price, 0);
      onSelectionChange(selectedAddOns, totalAddonPrice);
    }
  }, [selectedAddOns, onSelectionChange]);

  if (loading) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <div className="flex items-center justify-center space-x-2">
            <Loader2 className="h-5 w-5 animate-spin" />
            <span>Loading add-ons...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <div className="text-center text-red-600">
            <p>Error loading add-ons: {error}</p>
            {error.includes('No Ticket matches') && (
              <p className="text-sm text-gray-600 mt-2">
                This ticket may not exist. Please try selecting a different ticket.
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (categories.length === 0) {
    const itemName = itemType === 'destination' ? 'destination' : 'ticket';
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Star className="h-5 w-5 text-ghana-green" />
            <span>Customize Your Experience</span>
          </CardTitle>
          <CardDescription>
            No add-ons available for this {itemName}
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Star className="h-5 w-5 text-ghana-green" />
          <span>Customize Your Experience</span>
        </CardTitle>
        <CardDescription>
          Select upgrades and add-ons to enhance your tour
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {categories.map((category, categoryIndex) => (
          <div key={category.id}>
            {categoryIndex > 0 && <Separator />}
            
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                {React.createElement(getIconComponent(category.icon), {
                  className: "h-5 w-5 text-ghana-green"
                })}
                <h4 className="font-semibold">{category.name}</h4>
              </div>

              {category.addons.map((addon) => (
                <div key={addon.id}>
                  {addon.addon_type === 'multiple' ? (
                    // Multiple choice add-on (radio buttons)
                    <RadioGroup
                      value={getSelectedOption(addon.slug) || ''}
                      onValueChange={(value) => handleOptionChange(addon.slug, value, addon)}
                      className="space-y-2"
                    >
                      {/* Add a "None" option to allow deselection */}
                      <div className="flex items-center space-x-2 p-3 border rounded-lg bg-gray-50">
                        <RadioGroupItem value="" id={`${addon.slug}-none`} />
                        <Label htmlFor={`${addon.slug}-none`} className="flex-1 cursor-pointer">
                          <div className="flex justify-between items-center">
                            <div>
                              <p className="font-medium text-gray-600">Skip this option</p>
                              <p className="text-sm text-gray-500">No additional cost</p>
                            </div>
                            <span className="text-gray-500 font-medium">
                              GH₵0
                            </span>
                          </div>
                        </Label>
                      </div>
                      
                      {addon.options.map((option) => (
                        <div key={option.id} className="flex items-center space-x-2 p-3 border rounded-lg">
                          <RadioGroupItem value={option.id.toString()} id={`${addon.slug}-${option.id}`} />
                          <Label htmlFor={`${addon.slug}-${option.id}`} className="flex-1 cursor-pointer">
                            <div className="flex justify-between items-center">
                              <div>
                                <p className="font-medium">{option.name}</p>
                                {option.description && (
                                  <p className="text-sm text-gray-600">{option.description}</p>
                                )}
                              </div>
                              <span className="text-ghana-green font-medium">
                                {option.price > 0 ? `+GH₵${option.price.toLocaleString()}` : 'Included'}
                                {addon.pricing_type === 'per_person' && option.price > 0 && ' per person'}
                              </span>
                            </div>
                          </Label>
                        </div>
                      ))}
                    </RadioGroup>
                  ) : (
                    // Checkbox add-on
                    <div className="flex items-center space-x-3 p-3 border rounded-lg">
                      <Checkbox
                        id={addon.slug}
                        checked={isAddOnSelected(addon.id)}
                        onCheckedChange={(checked) => {
                          console.log(`🖱️ Checkbox clicked for ${addon.name}: ${checked}`);
                          handleAddOnToggle(addon, checked as boolean);
                        }}
                      />
                      <Label htmlFor={addon.slug} className="flex-1 cursor-pointer">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="font-medium">{addon.name}</p>
                            <p className="text-sm text-gray-600">{addon.description}</p>
                            {addon.features && addon.features.length > 0 && (
                              <div className="mt-2 space-y-1">
                                {addon.features.slice(0, 3).map((feature, index) => (
                                  <div key={index} className="flex items-center space-x-2 text-xs text-gray-500">
                                    <span className="w-1 h-1 bg-ghana-green rounded-full"></span>
                                    <span>{feature}</span>
                                  </div>
                                ))}
                                {addon.features.length > 3 && (
                                  <p className="text-xs text-gray-500">+{addon.features.length - 3} more features</p>
                                )}
                              </div>
                            )}
                          </div>
                          <div className="text-right">
                            <span className="text-ghana-green font-medium">
                              +GH₵{addon.calculated_price.toLocaleString()}
                            </span>
                            {addon.pricing_type === 'per_person' && (
                              <p className="text-xs text-gray-500">per person</p>
                            )}
                            {addon.pricing_type === 'per_group' && (
                              <p className="text-xs text-gray-500">per group</p>
                            )}
                          </div>
                        </div>
                      </Label>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}

        {selectedAddOns.length > 0 && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h5 className="font-medium text-gray-900 mb-2">Selected Add-ons:</h5>
            <div className="space-y-1">
              {selectedAddOns.map((addon, index) => (
                <div key={index} className="flex justify-between text-sm">
                  <span>{addon.name}</span>
                  <span className="text-ghana-green font-medium">
                    +GH₵{addon.total_price.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
            <Separator className="my-2" />
            <div className="flex justify-between font-medium">
              <span>Add-ons Total:</span>
              <span className="text-ghana-green">
                +GH₵{selectedAddOns.reduce((sum, addon) => sum + addon.total_price, 0).toLocaleString()}
              </span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AddOnSelector;