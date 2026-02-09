import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { CompassIcon, ChartUpIcon, FundraisingIcon, BridgeIcon } from './InfographicIcons';

gsap.registerPlugin(ScrollTrigger);

/**
 * Journey/Timeline section showing the 4-week accelerator phases
 */
const JourneySection = () => {
    const timelineRef = useRef(null);
    const lineRef = useRef(null);

    const phases = [
        {
            week: 'Week 1',
            title: 'Foundation',
            type: 'Virtual',
            description: 'Deep-dive workshops on product-market fit, user research, and building your 10x product.',
            IconComponent: CompassIcon,
        },
        {
            week: 'Week 2',
            title: 'Go-to-Market',
            type: 'Virtual',
            description: 'Sales strategy, pricing, distribution channels, and landing your first enterprise customers.',
            IconComponent: ChartUpIcon,
        },
        {
            week: 'Week 3',
            title: 'Fundraising',
            type: 'Virtual',
            description: 'Pitch deck mastery, investor psychology, term sheets, and negotiation tactics.',
            IconComponent: FundraisingIcon,
        },
        {
            week: 'Week 4',
            title: 'Silicon Valley',
            type: 'In-Person',
            description: 'Demo Day in SF, VC meetings, partner connections, and building your US presence.',
            IconComponent: BridgeIcon,
            highlight: true,
        },
    ];

    useEffect(() => {
        // Animate the connecting line drawing
        if (lineRef.current) {
            gsap.fromTo(
                lineRef.current,
                { height: '0%' },
                {
                    height: '100%',
                    duration: 1.5,
                    ease: 'power2.out',
                    scrollTrigger: {
                        trigger: timelineRef.current,
                        start: 'top 60%',
                    },
                }
            );
        }

        // Stagger animate the timeline items
        const items = timelineRef.current.querySelectorAll('.timeline-item');
        gsap.fromTo(
            items,
            { opacity: 0, x: -30 },
            {
                opacity: 1,
                x: 0,
                duration: 0.6,
                stagger: 0.15,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: timelineRef.current,
                    start: 'top 60%',
                },
            }
        );

        return () => {
            ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
        };
    }, []);

    return (
        <section id="journey" className="relative py-32 px-6">
            <div className="max-w-4xl mx-auto">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                    className="text-center mb-20"
                >
                    <h2 className="text-3xl md:text-5xl font-bold mb-4">
                        Your <span className="gradient-text">4-Week Workday</span>
                    </h2>
                    <p className="text-slate-400">
                        From foundation to fundraising, we've got you covered.
                    </p>
                </motion.div>

                {/* Timeline */}
                <div ref={timelineRef} className="relative">
                    {/* Connecting Line */}
                    <div className="absolute left-6 md:left-8 top-0 bottom-0 w-0.5 bg-white/10">
                        <div
                            ref={lineRef}
                            className="w-full bg-gradient-to-b from-z5-purple to-z5-pink"
                            style={{ height: '0%' }}
                        />
                    </div>

                    {/* Timeline Items */}
                    <div className="space-y-8">
                        {phases.map((phase, index) => (
                            <div
                                key={index}
                                className={`timeline-item relative pl-16 md:pl-20 opacity-0 ${phase.highlight ? 'highlight' : ''
                                    }`}
                            >
                                {/* Node */}
                                <div
                                    className={`absolute left-3 md:left-5 w-6 h-6 rounded-full border-2 
                    ${phase.highlight
                                            ? 'bg-gradient-to-r from-z5-purple to-z5-pink border-z5-pink animate-pulse-glow'
                                            : 'bg-z5-dark border-z5-purple/50'
                                        } z-10`}
                                />

                                {/* Card */}
                                <div
                                    className={`glass-card p-6 ${phase.highlight
                                        ? 'border-z5-pink/30 shadow-glow-pink'
                                        : ''
                                        }`}
                                >
                                    <div className="flex items-start gap-4">
                                        <phase.IconComponent size={36} />
                                        <div className="flex-1">
                                            <div className="flex items-center gap-3 mb-2">
                                                <span className="text-xs font-medium text-z5-purple uppercase tracking-wider">
                                                    {phase.week}
                                                </span>
                                                <span
                                                    className={`text-xs px-2 py-0.5 rounded-full ${phase.type === 'In-Person'
                                                        ? 'bg-z5-pink/20 text-z5-pink'
                                                        : 'bg-white/5 text-slate-400'
                                                        }`}
                                                >
                                                    {phase.type}
                                                </span>
                                            </div>
                                            <h3 className="text-xl font-bold text-white mb-2">
                                                {phase.title}
                                            </h3>
                                            <p className="text-sm text-slate-400 leading-relaxed">
                                                {phase.description}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
};

export default JourneySection;
