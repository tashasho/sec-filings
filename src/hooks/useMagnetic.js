import { useEffect } from 'react';
import gsap from 'gsap';

/**
 * Magnetic effect hook - pulls element toward cursor on hover
 * @param {React.RefObject} ref - Element reference
 * @param {number} strength - Pull strength (0-1), default 0.3
 */
const useMagnetic = (ref, strength = 0.3) => {
    useEffect(() => {
        const element = ref.current;
        if (!element) return;

        // Check if it's a touch device
        if (window.matchMedia('(hover: none)').matches) {
            return;
        }

        const handleMouseMove = (e) => {
            const rect = element.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;

            const x = e.clientX - centerX;
            const y = e.clientY - centerY;

            gsap.to(element, {
                x: x * strength,
                y: y * strength,
                duration: 0.3,
                ease: 'power2.out',
            });
        };

        const handleMouseLeave = () => {
            gsap.to(element, {
                x: 0,
                y: 0,
                duration: 0.5,
                ease: 'elastic.out(1, 0.3)',
            });
        };

        element.addEventListener('mousemove', handleMouseMove);
        element.addEventListener('mouseleave', handleMouseLeave);

        return () => {
            element.removeEventListener('mousemove', handleMouseMove);
            element.removeEventListener('mouseleave', handleMouseLeave);
        };
    }, [ref, strength]);
};

export default useMagnetic;
