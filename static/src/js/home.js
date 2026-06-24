const gridBtn = document.getElementById('gridBtn');
const listBtn = document.getElementById('listBtn');
const contentsWrapper = document.getElementById('grid-list-contents');

// লিস্ট ভিউ বাটনে ক্লিক করলে
listBtn.addEventListener('click', () => {
    gridBtn.classList.remove('active');
    listBtn.classList.add('active');
    contentsWrapper.classList.add('list-contents'); // লিস্ট ক্লাসে রূপান্তর
});

// গ্রিড ভিউ বাটনে ক্লিক করলে
gridBtn.addEventListener('click', () => {
    listBtn.classList.remove('active');
    gridBtn.classList.add('active');
    contentsWrapper.classList.remove('list-contents'); // গ্রিড ক্লাসে ফেরত নেওয়া
});