import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';
import FloatingFounderCard from './FloatingFounderCard';

/**
 * Community section with testimonials from portfolio companies and mentors
 * Includes floating orbs background animation
 */
const CommunitySection = () => {
    const orbsRef = useRef(null);

    // Animated floating orbs background
    useEffect(() => {
        if (!orbsRef.current) return;
        const orbs = orbsRef.current.querySelectorAll('.floating-orb');

        orbs.forEach((orb, i) => {
            gsap.to(orb, {
                x: `random(-100, 100)`,
                y: `random(-100, 100)`,
                duration: 8 + i * 2,
                repeat: -1,
                yoyo: true,
                ease: 'sine.inOut',
            });
        });
    }, []);

    const testimonials = [
        // Portfolio Companies
        {
            initial: 'A',
            name: 'Aditya R.',
            subtitle: 'IIT Bombay · AI Research',
            quote: 'Found my technical co-founder in Week 1. Closed seed in Week 5.',
            type: 'portfolio',
            image: null, // Replace with actual image path
        },
        {
            initial: 'P',
            name: 'Priya K.',
            subtitle: 'IIT Delhi · Enterprise SaaS',
            quote: 'From dorm room idea to $2M ARR in 8 months.',
            type: 'portfolio',
            image: null,
        },
        {
            initial: 'R',
            name: 'Rohan M.',
            subtitle: 'IIT Kanpur · DevTools',
            quote: 'The network alone is worth 10x the equity.',
            type: 'portfolio',
            image: null,
        },
        // Mentors
        {
            initial: 'S',
            name: 'Sneha V.',
            subtitle: 'Partner, Sequoia India',
            quote: 'The quality of founders in Ascend rivals any top accelerator globally.',
            type: 'mentor',
            image: null,
        },
        {
            initial: 'M',
            name: 'Mikhail T.',
            subtitle: 'Ex-CTO, Stripe',
            quote: 'These are the builders who will define India\'s next tech generation.',
            type: 'mentor',
            image: null,
        },
        {
            initial: 'L',
            name: 'Lisa C.',
            subtitle: 'GP, Accel',
            quote: 'Ascend founders come prepared. They know their market, customers, and metrics.',
            type: 'mentor',
            image: null,
        },
        // Additional portfolio
        {
            initial: 'V',
            name: 'Vikram S.',
            subtitle: 'IIT Madras · FinTech',
            quote: 'The mentorship in Week 3 completely transformed our fundraising strategy.',
            type: 'portfolio',
            image: null,
        },
        {
            initial: 'N',
            name: 'Neha G.',
            subtitle: 'IIT Kharagpur · HealthTech',
            quote: 'We landed our first enterprise client during Demo Day. Game changer.',
            type: 'portfolio',
            image: null,
        },
        // Additional mentor
        {
            initial: 'D',
            name: 'David K.',
            subtitle: 'Partner, a16z',
            quote: 'Ascend is producing the next wave of globally competitive Indian startups.',
            type: 'mentor',
            image: null,
        },
    ];

    return (
        <section id="community" className="relative py-32 px-6 overflow-hidden">
            {/* Floating Orbs Background */}
            <div ref={orbsRef} className="absolute inset-0 pointer-events-none overflow-hidden">
                <div className="floating-orb absolute top-1/4 left-1/4 w-64 h-64 bg-z5-purple/5 rounded-full blur-3xl" />
                <div className="floating-orb absolute top-1/2 right-1/4 w-96 h-96 bg-z5-pink/5 rounded-full blur-3xl" />
                <div className="floating-orb absolute bottom-1/4 left-1/3 w-80 h-80 bg-z5-purple/8 rounded-full blur-3xl" />
                <div className="floating-orb absolute top-1/3 right-1/3 w-48 h-48 bg-z5-pink/6 rounded-full blur-2xl" />
            </div>

            <div className="max-w-7xl mx-auto relative z-10">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <h2 className="text-3xl md:text-5xl font-bold mb-4">
                        You're joining a{' '}
                        <span className="gradient-text">movement</span>
                    </h2>
                    <p className="text-slate-400 max-w-2xl mx-auto">
                        Hear from our portfolio founders and mentors who've been part of the Ascend journey.
                    </p>
                </motion.div>

                {/* Testimonials Grid - 6 cards */}
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
                    {testimonials.map((founder, index) => (
                        <FloatingFounderCard key={index} founder={founder} index={index} />
                    ))}
                </div>
            </div>
        </section>
    );
};

export default CommunitySection;
