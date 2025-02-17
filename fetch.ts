import { getJWTtoken } from './authorization';
import type { Product } from '@/models/product/product';
import { toast } from 'sonner';

export const fetchProduct = async (sku: string): Promise<Product | null> => {
    return fetchWrapper<Product>(`/Product/${sku}`);
};

export const fetchWrapper = async <T>(url: string, key?: string | null, method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'GET', formData?: Record<string, unknown>, signal?: AbortController): Promise<T | null> => {
    const jwtToken = getJWTtoken();

    const baseHeaders: Record<string, unknown> = {
        "Authorization": `Bearer ${jwtToken || process.env.API_KEY!}`,
        "SiteId": process.env.SITE_ID!
    };

    return fetch(`${process.env.API_BASE}${url}`, {
        method: method,
        ...formData && { body: JSON.stringify(formData) },
        ...signal && { signal: signal.signal },
        headers: {
            ...baseHeaders,
            ...formData && { "Content-Type": "application/json" }
        }
    })
        .then((response) => response.json())
        .then((response) => {
            if (response.success) {
                return (key ? response.data[key] : response.data) as T;
            }
            else {
                if (response.message && toast.name) {
                    toast.error(response.message);
                }
                return null;
            }
        }).catch((error) => {
            console.log(error);
            return null;
        });
};

export const fetchProductImage = (src: string) => {
    return `${process.env.MEDIA_BASE}/Images/Productimages/${src}`;
};

export const fetchImage = (src: string) => {
    return `${process.env.MEDIA_BASE}/Images/${src}`;
};

export const fetchCategoryImage = (src: string) => {
    return `${process.env.MEDIA_BASE}/Images/ProductImages/Thumb/${src}`;
}