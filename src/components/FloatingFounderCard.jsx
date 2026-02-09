import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import gsap from 'gsap';

/**
 * Floating testimonial card with image placeholder and perpetual float animation
 */
const FloatingFounderCard = ({ founder, index }) => {
    const cardRef = useRef(null);

    useEffect(() => {
        // Check for reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        // Async floating animation with varied timing
        const animation = gsap.to(cardRef.current, {
            y: -15 + (index % 3) * 5,
            duration: 4 + (index % 3),
            repeat: -1,
            yoyo: true,
            ease: 'power1.inOut',
            delay: index * 0.2,
        });

        return () => animation.kill();
    }, [index]);

    return (
        <motion.div
            ref={cardRef}
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
            viewport={{ once: true, margin: '-50px' }}
            whileHover={{ scale: 1.02 }}
            className="glass-card p-6 will-change-transform"
        >
            <div className="flex items-start gap-4">
                {/* Image Placeholder */}
                <div className="flex-shrink-0">
                    {founder.image ? (
                        <img
                            src={founder.image}
                            alt={founder.name}
                            className="w-14 h-14 rounded-full object-cover border-2 border-white/10"
                        />
                    ) : (
                        <div className="w-14 h-14 bg-gradient-to-br from-z5-purple to-z5-pink rounded-full flex items-center justify-center text-xl font-bold text-white">
                            {founder.initial}
                        </div>
                    )}
                </div>

                <div className="flex-1 min-w-0">
                    {/* Name & Role */}
                    <h3 className="font-bold text-white mb-0.5">{founder.name}</h3>
                    <p className="text-xs text-slate-500 mb-2">{founder.subtitle}</p>

                    {/* Type Badge */}
                    {founder.type && (
                        <span className={`inline-block text-[10px] px-2 py-0.5 rounded-full mb-2 ${founder.type === 'mentor'
                                ? 'bg-z5-purple/20 text-z5-purple'
                                : 'bg-z5-pink/20 text-z5-pink'
                            }`}>
                            {founder.type === 'mentor' ? 'Mentor' : 'Portfolio'}
                        </span>
                    )}
                </div>
            </div>

            {/* Quote */}
            <p className="text-sm text-slate-400 italic leading-relaxed mt-4">
                "{founder.quote}"
            </p>
        </motion.div>
    );
};

export default FloatingFounderCard;
