import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * Three.js particle background with 800-1000 purple/pink particles
 * Mouse interaction creates subtle rotation/ripple effect
 */
const ParticleBackground = () => {
    const canvasRef = useRef(null);
    const animationRef = useRef(null);

    useEffect(() => {
        if (!canvasRef.current) return;

        // Check for reduced motion preference
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );

        const renderer = new THREE.WebGLRenderer({
            canvas: canvasRef.current,
            alpha: true,
            antialias: true,
        });

        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        camera.position.z = 5;

        // Create particles - reduced on mobile
        const isMobile = window.innerWidth < 768;
        const particlesCount = isMobile ? 400 : 900;
        const particlesGeometry = new THREE.BufferGeometry();
        const posArray = new Float32Array(particlesCount * 3);
        const colorsArray = new Float32Array(particlesCount * 3);

        // Purple: #8B5CF6 -> (0.545, 0.361, 0.965)
        // Pink: #EC4899 -> (0.925, 0.282, 0.600)
        const purple = new THREE.Color(0x8b5cf6);
        const pink = new THREE.Color(0xec4899);

        for (let i = 0; i < particlesCount; i++) {
            // Position
            posArray[i * 3] = (Math.random() - 0.5) * 12;     // x
            posArray[i * 3 + 1] = (Math.random() - 0.5) * 12; // y
            posArray[i * 3 + 2] = (Math.random() - 0.5) * 8;  // z

            // Color interpolation between purple and pink
            const mixFactor = Math.random();
            const color = purple.clone().lerp(pink, mixFactor);
            colorsArray[i * 3] = color.r;
            colorsArray[i * 3 + 1] = color.g;
            colorsArray[i * 3 + 2] = color.b;
        }

        particlesGeometry.setAttribute(
            'position',
            new THREE.BufferAttribute(posArray, 3)
        );
        particlesGeometry.setAttribute(
            'color',
            new THREE.BufferAttribute(colorsArray, 3)
        );

        const particlesMaterial = new THREE.PointsMaterial({
            size: isMobile ? 0.02 : 0.015,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true,
        });

        const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particlesMesh);

        let mouseX = 0;
        let mouseY = 0;
        let targetRotationX = 0;
        let targetRotationY = 0;

        const handleMouseMove = (e) => {
            mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        };

        if (!isMobile) {
            document.addEventListener('mousemove', handleMouseMove);
        }

        const animate = () => {
            animationRef.current = requestAnimationFrame(animate);

            if (!prefersReducedMotion) {
                // Smooth rotation following mouse
                targetRotationX = mouseY * 0.15;
                targetRotationY = mouseX * 0.15;

                particlesMesh.rotation.x += (targetRotationX - particlesMesh.rotation.x) * 0.02;
                particlesMesh.rotation.y += (targetRotationY - particlesMesh.rotation.y) * 0.02;

                // Constant slow rotation
                particlesMesh.rotation.y += 0.0003;
            }

            renderer.render(scene, camera);
        };

        animate();

        const handleResize = () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
            document.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('resize', handleResize);
            renderer.dispose();
            particlesGeometry.dispose();
            particlesMaterial.dispose();
        };
    }, []);

    return (
        <canvas
            ref={canvasRef}
            className="fixed top-0 left-0 w-full h-full pointer-events-none"
            style={{
                zIndex: 0,
                opacity: 0.4,
            }}
            aria-hidden="true"
        />
    );
};

export default ParticleBackground;
