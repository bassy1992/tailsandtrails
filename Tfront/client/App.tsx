import "./global.css";

import React from "react";
import { Toaster } from "@/components/ui/toaster";
import { createRoot } from "react-dom/client";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { ToastProvider } from "./contexts/ToastContext";
import ProtectedRoute from "./components/ProtectedRoute";
import ErrorBoundary from "./components/ErrorBoundary";
import SafeTooltipProvider from "./components/SafeTooltipProvider";
import Index from "./pages/Index";
import Destinations from "./pages/Destinations";
import Gallery from "./pages/Gallery";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import ForgotPassword from "./pages/ForgotPassword";
import TourDetails from "./pages/TourDetails";
import Contact from "./pages/Contact";
import About from "./pages/About";
import Dashboard from "./pages/Dashboard";
import Booking from "./pages/Booking";
import MomoCheckout from "./pages/MomoCheckout";
import PaymentProcessing from "./pages/PaymentProcessing";
import PaymentCallback from "./pages/PaymentCallback";
// StripeCheckout removed - using MTN MoMo only
import PaymentSuccess from "./pages/PaymentSuccess";
import Tickets from "./pages/Tickets";
import TicketBooking from "./pages/TicketBooking";
import TicketCheckout from "./pages/TicketCheckout";
import TicketPurchaseSuccess from "./pages/TicketPurchaseSuccess";
import Placeholder from "./pages/Placeholder";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Index />} />
      <Route path="/destinations" element={<Destinations />} />
      <Route path="/gallery" element={<Gallery />} />
      <Route path="/videos" element={<Gallery />} />
      <Route path="/destinations/:id" element={<Placeholder />} />
      <Route path="/tour/:id" element={<TourDetails />} />
      <Route path="/tickets" element={<Tickets />} />
      <Route path="/tickets/:slug" element={<TicketBooking />} />
      <Route path="/ticket-booking/:id" element={<TicketBooking />} />
      <Route path="/ticket-checkout" element={
        <ProtectedRoute>
          <TicketCheckout />
        </ProtectedRoute>
      } />
      <Route path="/ticket-purchase-success" element={
        <ProtectedRoute>
          <TicketPurchaseSuccess />
        </ProtectedRoute>
      } />
      <Route path="/tours" element={<Placeholder />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      <Route path="/booking/:id" element={<Booking />} />
      <Route path="/momo-checkout" element={<MomoCheckout />} />
      <Route path="/payment-processing/:reference" element={<PaymentProcessing />} />
      <Route path="/payment-callback" element={<PaymentCallback />} />
      {/* Stripe checkout removed - using MTN MoMo only */}
      <Route path="/payment-success" element={<PaymentSuccess />} />
      <Route path="/admin" element={<Placeholder />} />
      {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <React.StrictMode>
        <QueryClientProvider client={queryClient}>
          <SafeTooltipProvider>
            <Toaster />
            <Sonner />
            <BrowserRouter>
              <ToastProvider>
                <AuthProvider>
                  <AppRoutes />
                </AuthProvider>
              </ToastProvider>
            </BrowserRouter>
          </SafeTooltipProvider>
        </QueryClientProvider>
      </React.StrictMode>
    </ErrorBoundary>
  );
}

export default App;

const rootElement = document.getElementById("root");
if (!rootElement) throw new Error('Failed to find the root element');

const root = createRoot(rootElement);
root.render(<App />);
