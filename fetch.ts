export const fetchWrapper = async <T>(url: string, key?: string | null, method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' = 'GET', formData?: Record<string, unknown>, signal?: AbortController): Promise<T | null> => {
    return fetch(`${process.env.API_BASE}${url}`, {
        method: method,
        ...formData && { body: JSON.stringify(formData) },
        ...signal && { signal: signal.signal },
        headers: {
            ...formData && { "Content-Type": "application/json" }
        }
    })
        .then((response) => response.json())
        .then((response) => {
            if (response.success) {
                return (key ? response.data[key] : response.data) as T;
            }
            else {
                if (response.message) {
                    console.error(response.message)
                }
                return null;
            }
        }).catch((error) => {
            console.log(error);
            return null;
        });
};
