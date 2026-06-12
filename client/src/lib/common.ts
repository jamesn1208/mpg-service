import { useRouter } from 'vue-router'

const router = useRouter()

export function movePage(s: string) {
    router.push(s)
}

export function callAPI(path: string, method: string) {
    fetch(`${window.location.origin}${path}`, {
        method: method,
        credentials: 'include',
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
