// Simple fade-in effect for sections
document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll("section");
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.classList.add("fade-in");
            }
        });
    }, { threshold: 0.1 });

    sections.forEach(section => {
        section.classList.add("opacity-zero");
        observer.observe(section);
    });
});
