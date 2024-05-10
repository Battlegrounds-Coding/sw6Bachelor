function sleep(sec:number) : Promise<void>{
    return new Promise((res) => {
        setTimeout(() => { res() }, sec)
    })
}

