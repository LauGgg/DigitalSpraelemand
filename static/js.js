class Octopus {
    constructor(sliders, indicators) {
        this.sliders = sliders;
        this.auto = false
        this.max = 15;
        this.indicators = indicators;
        this.autoBut = document.querySelector('[data-automatic]');
        this.randSub = document.querySelector('[data-random_submit]');
        this.sub = document.querySelector('[data-submit]');
        let index = 0;
        for (index = 0; index < this.sliders.length; index++) {
            this.sliders[index].addEventListener("input", (event) => {
                this.update();
            })
        }
    }
    formatInput(value) {
        let result = ((value / 50) * this.max).toFixed(1);
        return result + "°";
    }

    reset() {
        let index = 0;
        for (index = 0; index < this.sliders.length; index++) {
            this.sliders[index].value = 50;
        }
    }
    async submit() {
        let index = 0;
        let output = [];
        for (index = 0; index < this.sliders.length; index++) {
            output.push(this.sliders[index].value);
        }
        console.log(output);
        let positions = {"positions": output}
        let query = `${window.origin}/send`
        await fetch(query, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(positions),
            cache: "no-cache",
            headers: new Headers({
                'content-type': 'application/json'
            })
        })
    }
    randomize() {
        let index = 0;
        for (index = 0; index < this.sliders.length; index++) {
            this.sliders[index].value = Math.floor(Math.random() * 101);
        }
    }
    update() {
        let index = 0;
        for (index = 0; index < this.sliders.length; index++) {
            let value = this.sliders[index].value - 50;
            this.indicators[index].innerHTML = this.formatInput(value);
            let colorstr = `rgb(${187 + (value / 50) * 34}, ${98 + (value / 50) * 46}, ${178 - (value / 50) * 77})`;
            this.indicators[index].style.color = colorstr;
        }
    }
    async automatic() {
        if (this.auto) {
            this.auto = false;
            this.autoBut.id = 'automatic-off';
            this.autoBut.innerHTML = 'Send Automatic Updates';
            this.randSub.id = 'enabled';
            this.sub.id = 'enabled';
        }
        else {
            this.auto = true;
            this.autoBut.id = 'automatic-on'; 
            this.autoBut.innerHTML = 'Cancel Automatic Updates';
            this.randSub.id = 'disabled';
            this.sub.id = 'disabled';
        }
        console.log("automatisk besked");
        let query = `${window.origin}/auto`;
        let autoOnOff = {"Auto": this.auto};
        await fetch(query, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(autoOnOff),
            cache: "no-cache",
            headers: new Headers({
                'content-type': 'application/json'
            })
        })

    }
}   

document.addEventListener('DOMContentLoaded', function(event) {
    const sliders = document.querySelectorAll('[data-range]');
    const indicators = document.querySelectorAll('[data-parag]');

    const Octo = new Octopus(sliders, indicators);
    Octo.update();

    const resetButtun = document.querySelector('[data-reset]');
    resetButtun.addEventListener("click", () => {
        Octo.reset();
        Octo.update();
    })
    const randomButton = document.querySelector('[data-random]');
    randomButton.addEventListener("click", () => {
        Octo.randomize();
        Octo.update();
    })
    const submit = document.querySelector('[data-submit]');
    submit.addEventListener("click", () => {
        if (!Octo.auto) {
            Octo.submit();
        }
    })
    const randomSubmit = document.querySelector('[data-random_submit]');
    randomSubmit.addEventListener("click", () => {
        if (!Octo.auto) {
            Octo.randomize();
            Octo.update();
            Octo.submit();
        }
    })
    const autoBut = document.querySelector('[data-automatic]');
    autoBut.addEventListener("click", () => {
        Octo.automatic();
    })
})