import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const typographyVariants = cva(
    "leading-tight text-foreground w-fit inline-block tracking-normal transition-colors",
    {
        variants: {
            variant: {
                h1: "text-3xl font-bold",
                h2: "text-2xl font-bold",
                h3: "text-xl font-medium",
                h4: "text-lg",
                h5: 'text-md',
                p: "text-base font-normal",
                small: "text-sm font-light",
                span: "text-base",
            },
            color: {
                primary: "text-primary",
                secondary: "text-secondary",
                accent: "text-accent",
                foreground: "text-foreground",
                muted: "text-muted-foreground",
                destructive: "text-destructive",
                white: "text-white",
                inherit: 'text-[inherit]',
                success: "text-green-600"
            },
            align: {
                left: "text-left",
                center: "text-center",
                right: "text-right",
            },
            font: {
                sans: "font-sans",
                serif: "font-serif",
                mono: "font-mono",
                inherit: "font-[inherit]",
            },
            weight: {
                light: "font-light",
                normal: "font-normal",
                medium: "font-medium",
                semibold: "font-semibold",
                bold: "font-bold",
                extrabold: "font-extrabold",
                black: "font-black",
            },
            size: {
                xs: "text-xs",
                sm: "text-sm",
                base: "text-base",
                md: 'text-md',
                lg: "text-lg",
                xl: "text-xl",
                "2xl": "text-2xl",
                "3xl": "text-3xl",
                "4xl": "text-4xl",
                "5xl": "text-5xl",
                "6xl": "text-6xl",
            }
        },
        defaultVariants: {
            variant: "p",
            color: "foreground",
            align: "left",
            font: "inherit",
            weight: 'normal',
        },
    }
);

export interface TypographyProps
    extends Omit<React.HTMLAttributes<HTMLElement>, 'color'>,
    VariantProps<typeof typographyVariants> {
}

const Typography = React.forwardRef<HTMLElement, TypographyProps>(
    ({ className, variant, color, align, weight, font, size, ...props }, ref) => {
        const Comp = variant;

        if (!Comp) {
            return;
        }

        return (
            <Comp
                className={cn(typographyVariants({ variant, color, align, font, size, weight, className }))}
                ref={ref as (React.Ref<HTMLHeadingElement> | undefined)}
                {...props}
            />
        );
    }
);

Typography.displayName = "Typography";

export { Typography, typographyVariants };
