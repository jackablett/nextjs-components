import { cn } from '@/lib/utils'
import React from 'react'

const Container = ({ children, className, style }: { children?: React.ReactNode, className?: string, style?: React.CSSProperties }) => {
    return (
        <div
            className={cn(
                'w-full mx-auto max-w-[1440px] px-4 relative md:px-12 2xl:px-0 z-[2]',
                className
            )}
            style={style}
        >
            {children}
        </div>
    )
}

export default Container