import Image from 'next/image';

const HeroImage = ({ src, alt, priority = false }) => {
  return (
    <div className="relative w-full h-full min-h-[60vh]">
      <Image
        src={`/images/hero/${src}`}
        alt={alt}
        fill
        style={{ objectFit: 'cover' }}
        quality={80}
        priority={priority}
        placeholder="blur"
        blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAADAAQDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=" // Low quality placeholder
      />
      {/* Overlay to improve text readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/20 to-black/40"></div>
    </div>
  );
};

export default HeroImage;