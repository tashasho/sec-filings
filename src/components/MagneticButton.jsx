import React, { useRef } from 'react';
import { motion } from 'framer-motion';
import useMagnetic from '../hooks/useMagnetic';

/**
 * Magnetic button wrapper - pulls toward cursor on hover
 * Uses spring physics for natural movement
 */
const MagneticButton = ({
    children,
    href,
    className = '',
    strength = 0.3,
    onClick,
    ...props
}) => {
    const buttonRef = useRef(null);
    useMagnetic(buttonRef, strength);

    const Component = href ? motion.a : motion.button;

    return (
        <Component
            ref={buttonRef}
            href={href}
            onClick={onClick}
            className={`magnetic-wrapper ${className}`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            transition={{
                type: 'spring',
                stiffness: 400,
                damping: 17,
            }}
            {...props}
        >
            {children}
        </Component>
    );
};

export default MagneticButton;
