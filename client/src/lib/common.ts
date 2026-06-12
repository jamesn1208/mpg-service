export function movePage(router: any, s: string) {
    router.push(s)
}

export function sleep(s: number) : Promise<void> {
    return new Promise(resolve => setTimeout(resolve, s * 1000));
}

export function callAPI(path: string, method: string, payload: any = {}) : any {
    fetch(`${window.location.origin}${path}`, {
        method: method,
        credentials: 'include',
        body: JSON.stringify(payload),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })
        .then(res => res.json())
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
