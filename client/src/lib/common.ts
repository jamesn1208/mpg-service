import { FAKE_USERNAMES } from "@/lib/data.ts";


export function movePage(router: any, s: string) {
    router.push(s)
}

export function sleep(s: number) : Promise<void> {
    return new Promise(resolve => setTimeout(resolve, s * 1000));
}

function extractFailReason(res: any) : string {
    const data = res.json()
    if (data.message && data.status === false) {
        return data.message;
    }
    return `HTTP ${res.status}: ${res.statusText}`;
}

export async function callAPI(path: string, method: string, payload: any = {}): Promise<any> {
    try {
        const res = await fetch(`${window.location.origin}${path}`, {
            method: method,
            credentials: 'include',
            body: JSON.stringify(payload),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        if (!res.ok) {
            throw new Error(extractFailReason(res))
        }
        return await res.json();
    } catch (reason: any) {
        console.error(reason.toString());
        throw new Error(reason);
    }
}

export function getFakeUsername() : string {
    return FAKE_USERNAMES[Math.floor(Math.random() * (FAKE_USERNAMES.length - 1))] as string;
}
