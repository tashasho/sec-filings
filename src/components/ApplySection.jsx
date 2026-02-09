import React from 'react';
import { motion } from 'framer-motion';
import MagneticButton from './MagneticButton';

/**
 * Apply section with CTA linking to external Typeform
 */
const ApplySection = () => {
    const typeformUrl = 'https://form.typeform.com/to/JypVl9Gh';

    return (
        <section id="apply" className="relative py-32 px-6">
            <div className="max-w-4xl mx-auto text-center">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                >
                    <h2 className="text-3xl md:text-5xl font-bold mb-4">
                        Ready to <span className="gradient-text">ascend?</span>
                    </h2>
                    <p className="text-slate-400 mb-12 max-w-xl mx-auto">
                        Applications close March 15, 2025. We review on a rolling basis. Response within 10 days of application
                    </p>
                </motion.div>

                {/* CTA Button */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    viewport={{ once: true }}
                >
                    <MagneticButton
                        href={typeformUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-3 px-12 py-5 rounded-full gradient-button text-xl"
                    >
                        Apply Now
                        <svg
                            className="w-5 h-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                        </svg>
                    </MagneticButton>
                </motion.div>

                {/* Contact Info */}
                <motion.p
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    viewport={{ once: true }}
                    className="text-sm text-slate-500 mt-12"
                >
                    Questions?{' '}
                    <a
                        href="mailto:apply@z5capital.com"
                        className="text-z5-purple hover:text-z5-pink underline transition-colors"
                    >
                        apply@z5capital.com
                    </a>
                </motion.p>
            </div>

            {/* Background Gradient */}
            <div className="absolute inset-0 -z-10">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-radial from-z5-purple/10 to-transparent rounded-full blur-3xl" />
            </div>
        </section>
    );
};

export default ApplySection;
