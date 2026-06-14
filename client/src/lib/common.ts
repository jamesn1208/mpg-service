import { FAKE_USERNAMES } from "@/lib/data.ts";


export function movePage(router: any, s: string) {
    router.push(s)
}

export function sleep(s: number) : Promise<void> {
    return new Promise(resolve => setTimeout(resolve, s * 1000));
}

export function callAPI(path: string, method: string, payload: any = {}) : Promise<any> {
    return fetch(`${window.location.origin}${path}`, {
        method: method,
        credentials: 'include',
        body: JSON.stringify(payload),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })
        .then(res => {
            if (!res.ok) {
                res.json().then(data => {
                    if (data.message && data.status === false) {
                        throw new Error(data.error_message)
                    }
                }).catch(_ => {
                    throw new Error(`HTTP ${res.status}: ${res.statusText}`)
                })
            }
            return res.json()
        })
        .then(data => {
            if (data.message && data.status === false) {
                throw new Error(data.error_message)
            }
            return data
        })
        .catch(reason => {
            console.error(reason.toString())
            throw new Error(reason)
        })
}

export function getFakeUsername() : string {
    return FAKE_USERNAMES[Math.floor(Math.random() * (FAKE_USERNAMES.length - 1))] as string;
}
