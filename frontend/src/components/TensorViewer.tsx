import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Line } from '@react-three/drei';
import * as THREE from 'three';

const SingularityCore = () => {
  const meshRef = useRef<THREE.Mesh>(null!);
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 3) * 0.2);
    }
  });
  return (
    <Sphere ref={meshRef} args={[0.5, 32, 32]} position={[0, 0, 0]}>
      <meshStandardMaterial color="#06b6d4" emissive="#06b6d4" emissiveIntensity={2} toneMapped={false} />
    </Sphere>
  );
};

const CubicGrid = () => {
  const groupRef = useRef<THREE.Group>(null!);
  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.005;
      groupRef.current.rotation.x += 0.002;
    }
  });

  const boxGeometry = new THREE.BoxGeometry(4, 4, 4);
  const edges = new THREE.EdgesGeometry(boxGeometry);

  return (
    <group ref={groupRef}>
      <lineSegments geometry={edges}>
        <lineBasicMaterial color="#4f46e5" transparent opacity={0.3} />
      </lineSegments>
      <Sphere args={[0.1, 16, 16]} position={[1.5, 0, 2.0]}>
        <meshBasicMaterial color="#ef4444" />
      </Sphere>
      <Line points={[[0, 0, 0], [1.5, 0, 2.0]]} color="#ef4444" lineWidth={2} dashed dashSize={0.2} gapSize={0.1} />
      <SingularityCore />
    </group>
  );
};

export default function TensorViewer() {
  return (
    <div className="w-full h-[400px] rounded-xl overflow-hidden border border-slate-700 bg-slate-900/50">
      <Canvas camera={{ position: [5, 5, 5], fov: 45 }}>
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <OrbitControls enableZoom={true} enablePan={false} autoRotate autoRotateSpeed={1.5} />
        <CubicGrid />
      </Canvas>
    </div>
  );
}
