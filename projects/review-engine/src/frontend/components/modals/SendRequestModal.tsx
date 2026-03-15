"use client";

import React, { useState, useEffect } from 'react';
import { X, UserPlus, Send, Search, Loader2 } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface Customer {
  id: number;
  name: string;
  email?: string;
  phone?: string;
}

interface SendRequestModalProps {
  isOpen: boolean;
  onClose: () => void;
  businessId: number;
}

export default function SendRequestModal({ isOpen, onClose, businessId }: SendRequestModalProps) {
  const [step, setStep] = useState<'select' | 'create'>('select');
  const [search, setSearch] = useState('');
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  const [newCustomer, setNewCustomer] = useState({
    name: '',
    email: '',
    phone: ''
  });

  // Fetch customers on search
  useEffect(() => {
    if (isOpen && search.length >= 2) {
      // Fetch from API
      // For MVP, we'll mock this for a second then show a result if it matches 'test'
      setLoading(true);
      const timer = setTimeout(() => {
        setCustomers([
          { id: 1, name: 'Sani Varada', email: 'sani@example.com', phone: '+919999999999' },
          { id: 2, name: 'John Smith', email: 'john@example.com' }
        ]);
        setLoading(false);
      }, 500);
      return () => clearTimeout(timer);
    } else {
      setCustomers([]);
    }
  }, [search, isOpen]);

  const handleSend = async (customerId: number) => {
    setSubmitting(true);
    try {
      const res = await fetch('http://localhost:8000/reviews/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_id: customerId, business_id: businessId })
      });
      if (res.ok) {
        onClose();
        // Trigger a refresh of the dashboard
        window.location.reload();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-md rounded-2xl shadow-2xl border border-slate-100 overflow-hidden animate-in zoom-in-95 duration-200">
        <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h2 className="text-xl font-bold text-slate-900">Send Review Request</h2>
          <button onClick={onClose} className="p-1 rounded-full hover:bg-slate-200 transition-colors">
            <X size={20} className="text-slate-500" />
          </button>
        </div>

        <div className="p-6">
          {step === 'select' ? (
            <div className="space-y-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                <input 
                  type="text"
                  placeholder="Search existing customer..."
                  className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>

              <div className="max-h-60 overflow-y-auto space-y-2 min-h-[100px]">
                {loading && (
                  <div className="flex justify-center py-8">
                    <Loader2 className="animate-spin text-slate-400" />
                  </div>
                )}
                
                {!loading && customers.length > 0 && customers.map((c) => (
                  <button 
                    key={c.id}
                    onClick={() => setSelectedCustomer(c)}
                    className={cn(
                      "w-full text-left p-3 rounded-xl border transition-all flex justify-between items-center",
                      selectedCustomer?.id === c.id ? "border-slate-900 bg-slate-900 text-white" : "border-slate-100 hover:border-slate-300 bg-slate-50 text-slate-700"
                    )}
                  >
                    <div>
                      <div className="font-semibold">{c.name}</div>
                      <div className={cn("text-xs", selectedCustomer?.id === c.id ? "text-slate-300" : "text-slate-500")}>
                        {c.phone || c.email}
                      </div>
                    </div>
                    {selectedCustomer?.id === c.id && <Send size={16} />}
                  </button>
                ))}

                {!loading && search.length >= 2 && customers.length === 0 && (
                  <div className="text-center py-8 text-slate-500 text-sm">No customers found.</div>
                )}
              </div>

              <div className="flex gap-3 pt-2">
                <button 
                  onClick={() => setStep('create')}
                  className="flex-1 py-2 px-4 border border-slate-200 rounded-xl font-medium text-slate-600 hover:bg-slate-50 transition-colors flex items-center justify-center gap-2"
                >
                  <UserPlus size={18} />
                  New Customer
                </button>
                <button 
                  disabled={!selectedCustomer || submitting}
                  onClick={() => selectedCustomer && handleSend(selectedCustomer.id)}
                  className="flex-1 py-2 px-4 bg-slate-900 text-white rounded-xl font-medium hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
                >
                  {submitting ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
                  Send Request
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4 animate-in slide-in-from-right-4 duration-300">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Full Name</label>
                <input 
                  type="text"
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all"
                  value={newCustomer.name}
                  onChange={(e) => setNewCustomer({...newCustomer, name: e.target.value})}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Phone Number</label>
                <input 
                  type="text"
                  placeholder="+1 (555) 000-0000"
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all"
                  value={newCustomer.phone}
                  onChange={(e) => setNewCustomer({...newCustomer, phone: e.target.value})}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700">Email Address (Optional)</label>
                <input 
                  type="email"
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all"
                  value={newCustomer.email}
                  onChange={(e) => setNewCustomer({...newCustomer, email: e.target.value})}
                />
              </div>
              
              <div className="flex gap-3 pt-4">
                <button 
                  onClick={() => setStep('select')}
                  className="px-4 py-2 font-medium text-slate-600 hover:bg-slate-50 rounded-xl transition-colors"
                >
                  Back
                </button>
                <button 
                  className="flex-1 py-2 px-4 bg-slate-900 text-white rounded-xl font-medium hover:bg-slate-800 transition-all flex items-center justify-center gap-2"
                  onClick={() => {
                    // Logic to create and then select
                    setStep('select');
                  }}
                >
                  Save & Select
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
