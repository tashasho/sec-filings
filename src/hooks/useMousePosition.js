import { useState, useEffect } from 'react';

/**
 * Track mouse position for particle interactions and cursor effects
 * @returns {{ x: number, y: number }} - Normalized mouse position (-1 to 1)
 */
const useMousePosition = () => {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseMove = (e) => {
            // Normalize to -1 to 1 range
            setMousePosition({
                x: (e.clientX / window.innerWidth) * 2 - 1,
                y: -(e.clientY / window.innerHeight) * 2 + 1,
            });
        };

        window.addEventListener('mousemove', handleMouseMove);

        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return mousePosition;
};

export default useMousePosition;
