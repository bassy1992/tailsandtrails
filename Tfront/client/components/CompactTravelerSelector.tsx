import { useState, useEffect } from "react";
import { Destination } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Users, TrendingDown } from "lucide-react";

interface CompactTravelerSelectorProps {
  destination: Destination;
  selectedTravelers: number;
  onTravelersChange: (travelers: number) => void;
  className?: string;
}

export default function CompactTravelerSelector({ 
  destination, 
  selectedTravelers, 
  onTravelersChange,
  className = ""
}: CompactTravelerSelectorProps) {
  const [options, setOptions] = useState<Array<{
    size: number;
    label: string;
    price: number;
    isDiscounted: boolean;
    savings?: number;
  }>>([]);

  useEffect(() => {
    const generateOptions = () => {
      const opts = [];
      const basePrice = parseFloat(destination.price);

      for (let i = 1; i <= destination.max_group_size; i++) {
        let price = basePrice;
        let isDiscounted = false;
        let savings = 0;

        // Find appropriate pricing tier if available
        if (destination.has_tiered_pricing && destination.pricing_tiers?.length) {
          const tier = destination.pricing_tiers.find(t => 
            i >= t.min_people && (t.max_people === null || i <= t.max_people)
          );
          
          if (tier) {
            price = parseFloat(tier.price_per_person);
            savings = basePrice - price;
            isDiscounted = savings > 0;
          }
        }

        opts.push({
          size: i,
          label: i === 1 ? "1 person" : `${i} people`,
          price,
          isDiscounted,
          savings: isDiscounted ? savings : undefined
        });
      }

      setOptions(opts);
    };

    generateOptions();
  }, [destination]);

  const selectedOption = options.find(opt => opt.size === selectedTravelers);

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Number of Travelers
        {destination.has_tiered_pricing && (
          <span className="text-xs text-green-600 ml-2">(Group discounts available)</span>
        )}
      </label>

      <Select 
        value={selectedTravelers.toString()} 
        onValueChange={(value) => onTravelersChange(Number(value))}
      >
        <SelectTrigger className="w-full">
          <SelectValue>
            {selectedOption && (
              <div className="flex items-center justify-between w-full">
                <span className="flex items-center">
                  <Users className="h-4 w-4 mr-2 text-gray-600" />
                  {selectedOption.label}
                </span>
                <div className="flex items-center space-x-2">
                  <span className="text-ghana-green font-medium">
                    GH₵{selectedOption.price.toLocaleString()}
                  </span>
                  {selectedOption.isDiscounted && (
                    <Badge variant="secondary" className="bg-green-100 text-green-800 text-xs">
                      Save GH₵{selectedOption.savings?.toFixed(0)}
                    </Badge>
                  )}
                </div>
              </div>
            )}
          </SelectValue>
        </SelectTrigger>
        
        <SelectContent>
          {options.map((option) => (
            <SelectItem key={option.size} value={option.size.toString()}>
              <div className="flex items-center justify-between w-full min-w-[300px]">
                <div className="flex items-center space-x-2">
                  <Users className="h-4 w-4 text-gray-600" />
                  <span>{option.label}</span>
                </div>
                
                <div className="flex items-center space-x-3">
                  <div className="text-right">
                    <div className="text-sm font-medium text-ghana-green">
                      GH₵{option.price.toLocaleString()} each
                    </div>
                    <div className="text-xs text-gray-500">
                      Total: GH₵{(option.price * option.size).toLocaleString()}
                    </div>
                  </div>
                  
                  {option.isDiscounted && option.savings && (
                    <Badge variant="secondary" className="bg-green-100 text-green-800 text-xs">
                      <TrendingDown className="h-3 w-3 mr-1" />
                      Save GH₵{option.savings.toFixed(0)}
                    </Badge>
                  )}
                </div>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {/* Clean Price Summary */}
      {selectedOption && (
        <div className="mt-3 p-3 bg-gray-50 rounded-lg">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">
              {selectedOption.label} × GH₵{selectedOption.price.toLocaleString()}
            </span>
            <div className="text-right">
              <div className="text-lg font-bold text-ghana-green">
                GH₵{(selectedOption.price * selectedTravelers).toLocaleString()}
              </div>
              {selectedOption.isDiscounted && selectedOption.savings && (
                <div className="text-xs text-green-600">
                  You save GH₵{(selectedOption.savings * selectedTravelers).toFixed(0)} total
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}