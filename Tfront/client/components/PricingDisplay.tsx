import { Badge } from "@/components/ui/badge";
import { Destination } from "@/lib/api";
import { TrendingDown } from "lucide-react";

interface PricingDisplayProps {
  destination: Destination;
  groupSize?: number;
  showTiers?: boolean;
  compact?: boolean;
}

export default function PricingDisplay({ 
  destination, 
  groupSize = 1, 
  showTiers = false,
  compact = false 
}: PricingDisplayProps) {
  // Calculate pricing based on tiers
  const getPrice = () => {
    if (!destination.has_tiered_pricing || !destination.pricing_tiers?.length) {
      return {
        price: parseFloat(destination.price),
        isDiscounted: false,
        originalPrice: null
      };
    }

    // Find the appropriate tier
    const tier = destination.pricing_tiers.find(tier => 
      groupSize >= tier.min_people && 
      (tier.max_people === null || groupSize <= tier.max_people)
    );

    if (tier) {
      const tierPrice = parseFloat(tier.price_per_person);
      const basePrice = parseFloat(destination.price);
      return {
        price: tierPrice,
        isDiscounted: tierPrice < basePrice,
        originalPrice: tierPrice < basePrice ? basePrice : null
      };
    }

    return {
      price: parseFloat(destination.price),
      isDiscounted: false,
      originalPrice: null
    };
  };

  const { price, isDiscounted, originalPrice } = getPrice();

  if (compact) {
    return (
      <div className="text-right">
        {isDiscounted && originalPrice && (
          <div className="text-sm text-gray-500 line-through">
            GH₵{originalPrice.toLocaleString()}
          </div>
        )}
        <div className="text-2xl font-bold text-ghana-green">
          GH₵{price.toLocaleString()}
        </div>
        <div className="text-sm text-gray-500">per person</div>
        {isDiscounted && (
          <Badge variant="secondary" className="bg-green-100 text-green-800 text-xs mt-1">
            <TrendingDown className="h-3 w-3 mr-1" />
            Group discount
          </Badge>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="flex items-baseline space-x-2">
        {isDiscounted && originalPrice && (
          <span className="text-lg text-gray-500 line-through">
            GH₵{originalPrice.toLocaleString()}
          </span>
        )}
        <span className="text-3xl font-bold text-ghana-green">
          GH₵{price.toLocaleString()}
        </span>
      </div>
      
      <div className="text-sm text-gray-500">per person</div>
      
      {isDiscounted && (
        <Badge variant="secondary" className="bg-green-100 text-green-800">
          <TrendingDown className="h-3 w-3 mr-1" />
          Save GH₵{((originalPrice || 0) - price).toFixed(2)}
        </Badge>
      )}

      {showTiers && destination.has_tiered_pricing && destination.pricing_tiers?.length > 0 && (
        <div className="text-xs text-gray-600 space-y-1">
          <div className="font-medium">Group pricing available:</div>
          {destination.pricing_tiers.slice(0, 3).map((tier, index) => (
            <div key={tier.id} className="flex justify-between">
              <span>{tier.group_size_display}:</span>
              <span>GH₵{parseFloat(tier.price_per_person).toLocaleString()}</span>
            </div>
          ))}
          {destination.pricing_tiers.length > 3 && (
            <div className="text-gray-500">+ more tiers available</div>
          )}
        </div>
      )}
    </div>
  );
}