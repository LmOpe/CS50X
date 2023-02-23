setInterval(timer, 1000);

function timer () {
    const time = new Date();

    document.querySelector('#time').innerHTML = time.toLocaleTimeString();
}

const popover = new bootstrap.Popover('.popover-dismiss', {
    trigger: 'focus'
})
