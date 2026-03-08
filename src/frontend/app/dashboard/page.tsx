"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import SendRequestModal from '@/components/modals/SendRequestModal';
import { Loader2, TrendingUp, Star, Users, ArrowUpRight } from 'lucide-react';

export default function DashboardPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [stats, setStats] = useState<any>(null);
  const [activity, setActivity] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const businessId = 1; // Hardcoded for MVP

  useEffect(() => {
    async function fetchData() {
      try {
        const [statsRes, activityRes] = await Promise.all([
          fetch(`http://localhost:8000/reviews/stats/${businessId}`),
          fetch(`http://localhost:8000/reviews/activity/${businessId}`)
        ]);
        
        if (statsRes.ok) setStats(await statsRes.json());
        if (activityRes.ok) setActivity(await activityRes.json());
      } catch (err) {
        console.error("Failed to fetch dashboard data", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [businessId]);

  if (loading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <Loader2 className="animate-spin text-slate-400" size={40} />
      </div>
    );
  }

  const chartData = [
    { name: 'Sent', value: stats?.sent || 0 },
    { name: 'Opened', value: stats?.opened || 0 },
    { name: 'High Rating', value: stats?.high_rating || 0 },
    { name: 'Feedback', value: stats?.private_feedback || 0 },
  ];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Dashboard</h1>
          <p className="text-slate-500 text-sm mt-1">Overview of your reputation metrics</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-slate-900 text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-slate-800 transition-all shadow-lg shadow-slate-900/10 hover:shadow-slate-900/20 active:scale-95 flex items-center gap-2"
        >
          Send Review Request
        </button>
      </div>

      <SendRequestModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        businessId={businessId}
      />

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="border-none shadow-sm bg-white/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <Users size={14} /> Total Requests
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900">{stats?.total || 0}</div>
            <div className="flex items-center gap-1 text-xs text-green-600 mt-1 font-medium">
              <TrendingUp size={12} /> +12% from last month
            </div>
          </CardContent>
        </Card>
        <Card className="border-none shadow-sm bg-white/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <Star size={14} className="fill-yellow-400 text-yellow-400" /> Average Rating
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900">{stats?.avg_rating || 0}</div>
            <p className="text-xs text-slate-500 mt-1 font-medium">Out of 5.0</p>
          </CardContent>
        </Card>
        <Card className="border-none shadow-sm bg-white/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
               Negative Feedback
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-red-600">{stats?.private_feedback || 0}</div>
            <p className="text-xs text-slate-500 mt-1 font-medium">Rating &lt; 4</p>
          </CardContent>
        </Card>
        <Card className="border-none shadow-sm bg-white/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <TrendingUp size={14} /> Conversion Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900">{stats?.conversion_rate || 0}%</div>
            <p className="text-xs text-slate-500 mt-1 font-medium">Opened to Completed</p>
          </CardContent>
        </Card>
        <Card className="border-none shadow-sm bg-white/50 backdrop-blur-sm">
          <CardHeader className="pb-2">
            <CardTitle className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <ArrowUpRight size={14} /> Public Redirects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-slate-900">{stats?.high_rating || 0}</div>
            <p className="text-xs text-slate-500 mt-1 font-medium">High-quality reviews</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="border-none shadow-sm overflow-hidden">
          <CardHeader className="bg-slate-50/50">
            <CardTitle className="text-lg">Request Analytics</CardTitle>
          </CardHeader>
          <CardContent className="h-80 pt-6">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                <Tooltip 
                  cursor={{ fill: '#f8fafc' }}
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)', padding: '12px' }}
                />
                <Bar dataKey="value" fill="#0f172a" radius={[6, 6, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="border-none shadow-sm overflow-hidden">
          <CardHeader className="bg-slate-50/50 flex flex-row items-center justify-between">
            <CardTitle className="text-lg">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-slate-100">
              {activity.length > 0 ? activity.map((act, i) => (
                <div key={i} className="flex items-center justify-between p-4 hover:bg-slate-50 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-600">
                      {act.name.charAt(0)}
                    </div>
                    <div>
                      <div className="font-semibold text-slate-900">{act.name}</div>
                      <div className="text-xs text-slate-500">
                        {new Date(act.updated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={cn(
                      "text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full inline-block",
                      act.status === 'COMPLETED' ? "bg-green-100 text-green-700" :
                      act.status === 'SENT' ? "bg-blue-100 text-blue-700" :
                      "bg-slate-100 text-slate-700"
                    )}>
                      {act.status}
                    </div>
                    <div className="text-xs font-bold text-slate-900 mt-1">
                      {act.rating ? `${act.rating} ★` : '--'}
                    </div>
                  </div>
                </div>
              )) : (
                <div className="p-8 text-center text-slate-500">No activity yet.</div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function cn(...inputs: any[]) {
  return inputs.filter(Boolean).join(' ');
}
