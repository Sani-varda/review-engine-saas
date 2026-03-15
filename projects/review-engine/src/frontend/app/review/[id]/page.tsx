"use client";

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Star, Loader2, CheckCircle2, MessageSquare, ArrowRight } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function ReviewLandingPage() {
  const { id } = useParams();
  const router = useRouter();
  
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [business, setBusiness] = useState<any>(null);
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [feedback, setFeedback] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch review request data
  useEffect(() => {
    async function fetchRequest() {
      try {
        const res = await fetch(`http://localhost:8000/reviews/${id}`);
        if (res.ok) {
          const data = await res.json();
          if (data.status === 'COMPLETED') {
            setSubmitted(true);
          }
          setBusiness(data);
        } else {
          setError("This review link has expired or is invalid.");
        }
      } catch (err) {
        setError("Could not connect to the review server.");
      } finally {
        setLoading(false);
      }
    }
    if (id) fetchRequest();
  }, [id]);

  const handleSubmit = async () => {
    if (rating === 0) return;
    setSubmitting(true);
    try {
      const res = await fetch(`http://localhost:8000/reviews/${id}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rating, feedback })
      });
      
      if (res.ok) {
        const result = await res.json();
        if (result.action === 'REDIRECT') {
          // Redirect to Google/Public profile
          window.location.href = result.url;
        } else {
          setSubmitted(true);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 text-center">
        <Loader2 className="animate-spin text-slate-900" size={40} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 text-center">
        <div className="max-w-md bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
          <div className="text-red-500 mb-4">⚠️</div>
          <h1 className="text-xl font-bold text-slate-900 mb-2">Oops!</h1>
          <p className="text-slate-500">{error}</p>
        </div>
      </div>
    );
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 text-center animate-in fade-in duration-500">
        <div className="max-w-md w-full bg-white p-10 rounded-3xl shadow-2xl shadow-slate-200 border border-slate-100">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 text-green-600">
            <CheckCircle2 size={40} />
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-4">Thank You!</h1>
          <p className="text-slate-600 leading-relaxed">
            Your feedback has been received. We value your input and will use it to improve our service.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 animate-in fade-in duration-500">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl shadow-slate-200 border border-slate-100 overflow-hidden">
        {/* Header Section */}
        <div className="bg-slate-900 p-8 text-center">
          <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mx-auto mb-4 backdrop-blur-md">
            <Star className="text-white fill-white" size={32} />
          </div>
          <h1 className="text-xl font-bold text-white tracking-tight">{business?.business_name}</h1>
          <p className="text-slate-400 text-sm mt-1">We value your experience</p>
        </div>

        {/* Content Section */}
        <div className="p-8 space-y-8">
          <div className="text-center">
            <h2 className="text-lg font-bold text-slate-900 mb-6">How was your visit?</h2>
            <div className="flex justify-center gap-2">
              {[1, 2, 3, 4, 5].map((s) => (
                <button
                  key={s}
                  onMouseEnter={() => setHoverRating(s)}
                  onMouseLeave={() => setHoverRating(0)}
                  onClick={() => setRating(s)}
                  className="transition-transform active:scale-90"
                >
                  <Star 
                    size={44} 
                    className={cn(
                      "transition-colors duration-200",
                      (hoverRating || rating) >= s ? "text-yellow-400 fill-yellow-400" : "text-slate-200"
                    )}
                  />
                </button>
              ))}
            </div>
            {rating > 0 && (
              <p className="text-sm font-semibold mt-4 text-slate-500 animate-in fade-in slide-in-from-bottom-1">
                {rating === 5 && "Excellent! Love it."}
                {rating === 4 && "Great experience!"}
                {rating === 3 && "It was okay."}
                {rating === 2 && "Could be better."}
                {rating === 1 && "Very disappointed."}
              </p>
            )}
          </div>

          {rating > 0 && rating < 4 && (
            <div className="space-y-3 animate-in fade-in slide-in-from-top-2">
              <label className="text-sm font-bold text-slate-700 flex items-center gap-2">
                <MessageSquare size={16} /> Tell us more
              </label>
              <textarea 
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900 transition-all min-h-[120px]"
                placeholder="How can we improve your next visit?"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
              />
            </div>
          )}

          <button
            disabled={rating === 0 || submitting}
            onClick={handleSubmit}
            className="w-full bg-slate-900 text-white py-4 rounded-2xl font-bold flex items-center justify-center gap-2 hover:bg-slate-800 disabled:opacity-30 transition-all shadow-xl shadow-slate-900/10 active:scale-95"
          >
            {submitting ? (
              <Loader2 className="animate-spin" size={20} />
            ) : (
              <>
                {rating >= 4 ? "Continue to Google" : "Submit Feedback"}
                <ArrowRight size={20} />
              </>
            )}
          </button>
        </div>
        
        <div className="bg-slate-50 p-4 text-center">
          <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
            Powered by The Review Engine
          </p>
        </div>
      </div>
    </div>
  );
}
