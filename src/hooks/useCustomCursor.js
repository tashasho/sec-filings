import { useEffect, useCallback } from 'react';

/**
 * Custom cursor hook - creates a 20px circle that expands to 40px on interactive elements
 * Uses mix-blend-mode: difference for visibility on any background
 */
const useCustomCursor = () => {
    const updateCursorSize = useCallback((isHovering) => {
        const cursor = document.getElementById('custom-cursor');
        if (!cursor) return;

        if (isHovering) {
            cursor.style.width = '40px';
            cursor.style.height = '40px';
            cursor.style.borderWidth = '3px';
            cursor.style.backgroundColor = 'rgba(139, 92, 246, 0.1)';
        } else {
            cursor.style.width = '20px';
            cursor.style.height = '20px';
            cursor.style.borderWidth = '2px';
            cursor.style.backgroundColor = 'transparent';
        }
    }, []);

    useEffect(() => {
        // Check if it's a touch device
        if (window.matchMedia('(hover: none)').matches) {
            return;
        }

        const cursor = document.createElement('div');
        cursor.id = 'custom-cursor';
        cursor.style.cssText = `
      position: fixed;
      width: 20px;
      height: 20px;
      border: 2px solid rgba(139, 92, 246, 0.8);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      transition: width 0.2s ease, height 0.2s ease, border-width 0.2s ease, background-color 0.2s ease;
      mix-blend-mode: difference;
      transform: translate(-50%, -50%);
      background-color: transparent;
    `;
        document.body.appendChild(cursor);

        const moveCursor = (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        };

        const handleMouseEnter = (e) => {
            const target = e.target;
            if (
                target.tagName === 'A' ||
                target.tagName === 'BUTTON' ||
                target.closest('a') ||
                target.closest('button') ||
                target.classList.contains('magnetic-wrapper') ||
                target.closest('.magnetic-wrapper')
            ) {
                updateCursorSize(true);
            }
        };

        const handleMouseLeave = () => {
            updateCursorSize(false);
        };

        document.addEventListener('mousemove', moveCursor);
        document.addEventListener('mouseover', handleMouseEnter);
        document.addEventListener('mouseout', handleMouseLeave);

        return () => {
            document.removeEventListener('mousemove', moveCursor);
            document.removeEventListener('mouseover', handleMouseEnter);
            document.removeEventListener('mouseout', handleMouseLeave);
            if (document.body.contains(cursor)) {
                document.body.removeChild(cursor);
            }
        };
    }, [updateCursorSize]);
};

export default useCustomCursor;
