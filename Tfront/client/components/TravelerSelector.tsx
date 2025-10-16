import { useState, useEffect } from "react";
import { Destination, PricingTier } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Users, TrendingDown, Check } from "lucide-react";

interface TravelerSelectorProps {
  destination: Destination;
  selectedTravelers: number;
  onTravelersChange: (travelers: number) => void;
  className?: string;
}

export default function TravelerSelector({ 
  destination, 
  selectedTravelers, 
  onTravelersChange,
  className = ""
}: TravelerSelectorProps) {
  const [groupOptions, setGroupOptions] = useState<Array<{
    size: number;
    label: string;
    price: number;
    isDiscounted: boolean;
    savings?: number;
    tier?: PricingTier;
  }>>([]);

  useEffect(() => {
    const generateGroupOptions = () => {
      const options = [];
      const basePrice = parseFloat(destination.price);

      // If no pricing tiers, just create simple options
      if (!destination.has_tiered_pricing || !destination.pricing_tiers?.length) {
        for (let i = 1; i <= destination.max_group_size; i++) {
          options.push({
            size: i,
            label: i === 1 ? "1 person" : `${i} people`,
            price: basePrice,
            isDiscounted: false
          });
        }
        setGroupOptions(options);
        return;
      }

      // Create options based on pricing tiers
      const tiers = destination.pricing_tiers.sort((a, b) => a.min_people - b.min_people);
      
      for (let i = 1; i <= destination.max_group_size; i++) {
        // Find the appropriate tier for this group size
        const tier = tiers.find(t => 
          i >= t.min_people && (t.max_people === null || i <= t.max_people)
        );

        const price = tier ? parseFloat(tier.price_per_person) : basePrice;
        const savings = basePrice - price;

        options.push({
          size: i,
          label: i === 1 ? "1 person" : `${i} people`,
          price: price,
          isDiscounted: savings > 0,
          savings: savings > 0 ? savings : undefined,
          tier: tier
        });
      }

      setGroupOptions(options);
    };

    generateGroupOptions();
  }, [destination]);

  // Group options by pricing tiers for better display
  const groupedOptions = () => {
    if (!destination.has_tiered_pricing || !destination.pricing_tiers?.length) {
      return [{ tier: null, options: groupOptions }];
    }

    const groups: Array<{ tier: PricingTier | null; options: typeof groupOptions }> = [];
    const tiers = destination.pricing_tiers.sort((a, b) => a.min_people - b.min_people);

    tiers.forEach(tier => {
      const tierOptions = groupOptions.filter(option => 
        option.size >= tier.min_people && 
        (tier.max_people === null || option.size <= tier.max_people)
      );
      
      if (tierOptions.length > 0) {
        groups.push({ tier, options: tierOptions });
      }
    });

    return groups;
  };

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700 mb-3">
        Number of Travelers
        {destination.has_tiered_pricing && (
          <span className="text-xs text-gray-500 ml-2">
            (Group discounts available)
          </span>
        )}
      </label>

      <div className="space-y-3">
        {destination.has_tiered_pricing && destination.pricing_tiers?.length > 0 ? (
          // Pricing tier-based display
          groupedOptions().map((group, groupIndex) => (
            <div key={groupIndex}>
              {group.tier && (
                <div className="text-xs font-medium text-gray-600 mb-2 flex items-center">
                  <Users className="h-3 w-3 mr-1" />
                  {group.tier.group_size_display} - GH₵{parseFloat(group.tier.price_per_person).toLocaleString()} per person
                  {parseFloat(group.tier.price_per_person) < parseFloat(destination.price) && (
                    <Badge variant="secondary" className="ml-2 bg-green-100 text-green-800 text-xs">
                      <TrendingDown className="h-3 w-3 mr-1" />
                      Save GH₵{(parseFloat(destination.price) - parseFloat(group.tier.price_per_person)).toFixed(2)}
                    </Badge>
                  )}
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-2">
                {group.options.map((option) => (
                  <Card
                    key={option.size}
                    className={`cursor-pointer transition-all hover:shadow-md ${
                      selectedTravelers === option.size
                        ? 'ring-2 ring-ghana-green bg-ghana-green/5'
                        : 'hover:bg-gray-50'
                    }`}
                    onClick={() => onTravelersChange(option.size)}
                  >
                    <CardContent className="p-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Users className="h-4 w-4 text-gray-600" />
                          <span className="text-sm font-medium">{option.label}</span>
                          {selectedTravelers === option.size && (
                            <Check className="h-4 w-4 text-ghana-green" />
                          )}
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-semibold text-ghana-green">
                            GH₵{option.price.toLocaleString()}
                          </div>
                          <div className="text-xs text-gray-500">per person</div>
                        </div>
                      </div>
                      
                      {option.isDiscounted && option.savings && (
                        <div className="mt-2 text-xs text-green-600 flex items-center">
                          <TrendingDown className="h-3 w-3 mr-1" />
                          Save GH₵{option.savings.toFixed(2)} per person
                        </div>
                      )}
                      
                      <div className="mt-1 text-xs text-gray-500">
                        Total: GH₵{(option.price * option.size).toLocaleString()}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          ))
        ) : (
          // Simple display for destinations without pricing tiers
          <div className="grid grid-cols-2 gap-2">
            {groupOptions.map((option) => (
              <Card
                key={option.size}
                className={`cursor-pointer transition-all hover:shadow-md ${
                  selectedTravelers === option.size
                    ? 'ring-2 ring-ghana-green bg-ghana-green/5'
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => onTravelersChange(option.size)}
              >
                <CardContent className="p-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Users className="h-4 w-4 text-gray-600" />
                      <span className="text-sm font-medium">{option.label}</span>
                      {selectedTravelers === option.size && (
                        <Check className="h-4 w-4 text-ghana-green" />
                      )}
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-semibold text-ghana-green">
                        GH₵{option.price.toLocaleString()}
                      </div>
                      <div className="text-xs text-gray-500">per person</div>
                    </div>
                  </div>
                  
                  <div className="mt-1 text-xs text-gray-500">
                    Total: GH₵{(option.price * option.size).toLocaleString()}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Summary */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">
            Selected: {selectedTravelers} {selectedTravelers === 1 ? 'person' : 'people'}
          </span>
          <div className="text-right">
            {(() => {
              const selectedOption = groupOptions.find(opt => opt.size === selectedTravelers);
              if (!selectedOption) return null;
              
              return (
                <>
                  <div className="text-lg font-bold text-ghana-green">
                    GH₵{(selectedOption.price * selectedTravelers).toLocaleString()}
                  </div>
                  <div className="text-xs text-gray-500">
                    GH₵{selectedOption.price.toLocaleString()} × {selectedTravelers}
                  </div>
                  {selectedOption.isDiscounted && selectedOption.savings && (
                    <div className="text-xs text-green-600">
                      Save GH₵{(selectedOption.savings * selectedTravelers).toFixed(2)} total
                    </div>
                  )}
                </>
              );
            })()}
          </div>
        </div>
      </div>
    </div>
  );
}