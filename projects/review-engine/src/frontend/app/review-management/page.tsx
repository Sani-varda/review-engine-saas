"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Star, MessageSquare, Send, Sparkles, CheckCircle2 } from 'lucide-react';

export default function ReviewManagementPage() {
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generatingId, setGeneratingId] = useState<string | null>(null);
  const [replies, setReplies] = useState<{[key: string]: string}>({});

  const businessId = 1;

  useEffect(() => {
    async function fetchReviews() {
      try {
        const res = await fetch(`http://localhost:8000/google/reviews?business_id=${businessId}`, {
          headers: { 'Authorization': 'Bearer dummy-token' }
        });
        if (res.ok) {
          const data = await res.json();
          setReviews(data);
        }
      } catch (err) {
        console.error("Failed to fetch reviews", err);
      } finally {
        setLoading(false);
      }
    }
    fetchReviews();
  }, [businessId]);

  const generateAIReply = async (review: any) => {
    setGeneratingId(review.reviewId);
    // Mocking AI generation delay
    setTimeout(() => {
      const mockReply = `Hi ${review.reviewer.displayName}, thank you so much for your ${review.starRating.toLowerCase()} star review! We're glad you enjoyed your experience.`;
      setReplies(prev => ({ ...prev, [review.reviewId]: mockReply }));
      setGeneratingId(null);
    }, 1500);
  };

  const submitReply = async (reviewId: string) => {
    const replyText = replies[reviewId];
    if (!replyText) return;

    try {
      const res = await fetch(`http://localhost:8000/google/reviews/${reviewId}/reply?business_id=${businessId}&reply_text=${encodeURIComponent(replyText)}`, {
        method: 'POST',
        headers: { 'Authorization': 'Bearer dummy-token' }
      });
      if (res.ok) {
        // Update local state to show it's replied
        setReviews(prev => prev.map(r => 
          r.reviewId === reviewId ? { ...r, reply: { comment: replyText } } : r
        ));
      }
    } catch (err) {
      console.error("Failed to submit reply", err);
    }
  };

  if (loading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <Loader2 className="animate-spin text-slate-400" size={40} />
      </div>
    );
  }

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Review Management</h1>
        <p className="text-slate-500 text-sm mt-1">Monitor and reply to your Google Business reviews</p>
      </div>

      <div className="space-y-6">
        {reviews.map((review) => (
          <Card key={review.reviewId} className="border-none shadow-sm overflow-hidden">
            <CardContent className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-600 text-lg">
                    {review.reviewer.displayName.charAt(0)}
                  </div>
                  <div>
                    <div className="font-bold text-slate-900 text-lg">{review.reviewer.displayName}</div>
                    <div className="flex gap-0.5 mt-0.5">
                      {[...Array(5)].map((_, i) => (
                        <Star 
                          key={i} 
                          size={14} 
                          className={i < (review.starRating === 'FIVE' ? 5 : 4) ? "fill-yellow-400 text-yellow-400" : "text-slate-200"} 
                        />
                      ))}
                    </div>
                  </div>
                </div>
                <div className="text-xs text-slate-400 font-medium">
                  {new Date(review.createTime).toLocaleDateString()}
                </div>
              </div>

              <p className="text-slate-700 leading-relaxed mb-6">"{review.comment}"</p>

              {review.reply ? (
                <div className="bg-slate-50 rounded-xl p-4 border border-slate-100">
                  <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">
                    <CheckCircle2 size={12} className="text-green-500" /> Your Reply
                  </div>
                  <p className="text-slate-600 text-sm italic">{review.reply.comment}</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex gap-3">
                    <textarea 
                      value={replies[review.reviewId] || ''}
                      onChange={(e) => setReplies(prev => ({ ...prev, [review.reviewId]: e.target.value }))}
                      placeholder="Write your reply..."
                      className="w-full bg-slate-50 border-none rounded-xl p-4 text-sm focus:ring-2 focus:ring-slate-200 transition-all min-h-[100px] resize-none"
                    />
                  </div>
                  <div className="flex justify-between items-center">
                    <button 
                      onClick={() => generateAIReply(review)}
                      disabled={generatingId === review.reviewId}
                      className="flex items-center gap-2 text-indigo-600 font-bold text-sm hover:text-indigo-700 transition-colors disabled:opacity-50"
                    >
                      {generatingId === review.reviewId ? (
                        <><Loader2 size={16} className="animate-spin" /> Thinking...</>
                      ) : (
                        <><Sparkles size={16} /> Generate AI Reply</>
                      )}
                    </button>
                    <button 
                      onClick={() => submitReply(review.reviewId)}
                      disabled={!replies[review.reviewId]}
                      className="bg-slate-900 text-white px-6 py-2 rounded-lg font-bold text-sm hover:bg-slate-800 transition-all flex items-center gap-2 disabled:opacity-50 shadow-md"
                    >
                      <Send size={14} /> Post Reply
                    </button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
