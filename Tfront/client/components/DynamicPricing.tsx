import { useState, useEffect } from "react";
import { destinationsApi, PricingResponse, Destination } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Loader2, Users, TrendingDown } from "lucide-react";

interface DynamicPricingProps {
  destination: Destination;
  groupSize: number;
  onPricingChange?: (pricing: PricingResponse) => void;
  showTiers?: boolean;
}

export default function DynamicPricing({ 
  destination, 
  groupSize, 
  onPricingChange,
  showTiers = false 
}: DynamicPricingProps) {
  const [pricing, setPricing] = useState<PricingResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPricing = async () => {
      if (!destination.id || groupSize < 1) return;

      setLoading(true);
      setError(null);

      try {
        const pricingData = await destinationsApi.getDestinationPricing(destination.id, groupSize);
        setPricing(pricingData);
        onPricingChange?.(pricingData);
      } catch (err) {
        console.error('Error fetching pricing:', err);
        setError('Failed to load pricing');
        // Fallback to base price
        const fallbackPricing: PricingResponse = {
          destination_id: destination.id,
          destination_name: destination.name,
          group_size: groupSize,
          price_per_person: destination.price,
          total_price: (parseFloat(destination.price) * groupSize).toFixed(2),
          base_price: destination.price,
          has_tiered_pricing: false,
          pricing_tiers: []
        };
        setPricing(fallbackPricing);
        onPricingChange?.(fallbackPricing);
      } finally {
        setLoading(false);
      }
    };

    fetchPricing();
  }, [destination.id, groupSize, onPricingChange]);

  if (loading) {
    return (
      <div className="flex items-center space-x-2 text-gray-500">
        <Loader2 className="h-4 w-4 animate-spin" />
        <span className="text-sm">Calculating price...</span>
      </div>
    );
  }

  if (error && !pricing) {
    return (
      <div className="text-red-500 text-sm">
        {error}
      </div>
    );
  }

  if (!pricing) {
    return null;
  }

  const basePrice = parseFloat(pricing.base_price);
  const currentPrice = parseFloat(pricing.price_per_person);
  const savings = basePrice - currentPrice;
  const savingsPercentage = basePrice > 0 ? ((savings / basePrice) * 100) : 0;

  return (
    <div className="space-y-4">
      {/* Main Price Display */}
      <div>
        <div className="text-3xl font-bold text-ghana-green mb-1">
          GH₵{parseFloat(pricing.price_per_person).toLocaleString()}
        </div>
        <div className="text-sm text-gray-500 mb-2">per person</div>
        
        {/* Show savings if applicable */}
        {pricing.has_tiered_pricing && savings > 0 && (
          <Badge variant="secondary" className="bg-green-100 text-green-800 text-xs">
            <TrendingDown className="h-3 w-3 mr-1" />
            Save GH₵{savings.toFixed(0)} ({savingsPercentage.toFixed(0)}%)
          </Badge>
        )}
      </div>
      
      {/* Group Size and Total */}
      <div className="bg-gray-50 p-3 rounded-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Users className="h-4 w-4" />
            <span>{groupSize} {groupSize === 1 ? 'person' : 'people'}</span>
          </div>
          <div className="text-right">
            <div className="text-lg font-semibold text-gray-900">
              GH₵{parseFloat(pricing.total_price).toLocaleString()}
            </div>
            <div className="text-xs text-gray-500">total</div>
          </div>
        </div>
      </div>

      {/* Pricing Tiers Display */}
      {showTiers && pricing.has_tiered_pricing && pricing.pricing_tiers.length > 0 && (
        <div className="border-t pt-3">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Group Pricing</h4>
          <div className="space-y-1">
            {pricing.pricing_tiers.map((tier) => {
              const isCurrentTier = groupSize >= tier.min_people && 
                                  (tier.max_people === null || groupSize <= tier.max_people);
              
              return (
                <div
                  key={tier.id}
                  className={`flex justify-between items-center text-sm p-2 rounded ${
                    isCurrentTier 
                      ? 'bg-ghana-green/10 border border-ghana-green/20' 
                      : 'bg-gray-50'
                  }`}
                >
                  <span className={isCurrentTier ? 'font-medium' : ''}>
                    {tier.group_size_display}
                  </span>
                  <span className={isCurrentTier ? 'font-medium text-ghana-green' : 'text-gray-600'}>
                    GH₵{parseFloat(tier.price_per_person).toLocaleString()}
                  </span>
                </div>
              );
            })}
          </div>
          
          <div className="text-xs text-gray-500 mt-2">
            💡 Larger groups get better rates automatically
          </div>
        </div>
      )}

      {/* Error indicator */}
      {error && (
        <div className="text-xs text-amber-600 bg-amber-50 p-2 rounded">
          ⚠️ Using fallback pricing. {error}
        </div>
      )}
    </div>
  );
}