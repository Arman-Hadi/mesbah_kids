import { normalizeNumbers } from './normalizeNumber.js';
import { filterCards } from './searchCards.js';


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const accessDeniedToast = document.getElementById('access-denied-toast');
function change_status(status, req_id, modal) {
    axios.post(
        api + "/api/status",
        { id: req_id, status: status },
        { headers: { 'X-CSRFToken': csrftoken } }
    ).then(() => {
        modal.hide();
        console.log("Sent!", req);
    }).catch(error => {
        if (error.response && error.response.status === 403) {
            accessDeniedToast.classList.add('show')

            setTimeout(() => {

                accessDeniedToast.classList.remove('show')
            }, 3000)
            // Handle 403 Forbidden error
            console.error('403 Forbidden: You do not have permission to perform this action.');
            // Optionally, you can display a user-friendly message or perform some other action
        }
    });
}

const api = window.location.origin

const card = document
    .getElementById("card-template")
    .content.querySelector(".card");

const deliverRequestsContainer = document.getElementById("deliver-requests");
const sentContainer = document.getElementById("sent");
const deliveredContainer = document.getElementById("delivered");

const badge1 = document.getElementById("badge1")
const badge2 = document.getElementById("badge2")
const badge3 = document.getElementById("badge3")

let deliverRequests = [];

UpdatingUI();
setInterval(UpdatingUI, 1000);
function UpdatingUI() {
    axios.get(api + "/api/kids?" + "exclude=IN&exclude=NO&gender=MA").then((res) => {
        const results = [...res.data];
        if (JSON.stringify(deliverRequests) !== JSON.stringify(results)) {
            deliverRequests = results;

            deliverRequestsContainer.innerHTML = "";
            sentContainer.innerHTML = "";
            deliveredContainer.innerHTML = "";

            deliverRequests.forEach((req) => {
                const PersonalCard = card.cloneNode(true);
                const name = req.first_name + ' ' + req.last_name;
                PersonalCard.setAttribute("data-search", normalizeNumbers(req.number, true) + ' ' + name);
                PersonalCard.querySelector(".card-header").textContent = req.gate_out === "FE" ? "مادر" : "پدر";
                PersonalCard.querySelector(".card-title").textContent = normalizeNumbers(req.number, true);
                PersonalCard.querySelector(".card-text").textContent = name;
                const datetime = new Date(req.last_change);
                const now = new Date();
                var delta = now - datetime;
                var minutes = Math.floor(delta / 60000);
                // PersonalCard.querySelector(".card-footer").textContent = datetime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false});
                PersonalCard.querySelector(".card-footer").textContent = `${minutes} دقیقه پیش`;
                if (req.status === "RE") {
                    req.gate_out === "FE"
                        ? PersonalCard.classList.add("text-bg-success")
                        : PersonalCard.classList.add("text-bg-primary");

                    const modalDOM = document.getElementById("myModal");
                    PersonalCard.addEventListener("click", () => {
                        const newModal = modalDOM.cloneNode(true);
                        document.body.appendChild(newModal);
                        newModal.addEventListener('hidden.bs.modal', () => {
                            newModal.remove();
                        })
                        const myModal = new bootstrap.Modal(newModal, {});
                        myModal.show();
                        newModal.querySelector(".modal-body").textContent = req.first_name + ' ' + req.last_name;
                        const successBtnEventListener = newModal
                            .querySelector(".btn-success")
                            .addEventListener("click", () => {
                                change_status('SE', req.id, myModal)
                            });
                    });

                    deliverRequestsContainer.appendChild(PersonalCard);

                    // navigator.vibrate([200])
                } else if (req.status == 'SE') {
                    req.gate_out === "FE"
                        ? PersonalCard.classList.add("text-bg-warning")
                        : PersonalCard.classList.add("text-bg-info");

                    const modalDOM2 = document.getElementById("myModal2");
                    PersonalCard.addEventListener("click", () => {
                        const newModal2 = modalDOM2.cloneNode(true);
                        document.body.appendChild(newModal2);
                        newModal2.addEventListener('hidden.bs.modal', () => {
                            newModal2.remove();
                        })
                        const myModal = new bootstrap.Modal(newModal2, {});
                        myModal.show();
                        newModal2.querySelector(".modal-body").textContent = req.first_name + ' ' + req.last_name;
                        const successBtnEventListener = newModal2
                            .querySelector(".btn-success")
                            .addEventListener("click", () => {
                                change_status('DE', req.id, myModal)
                            });
                    });

                    sentContainer.appendChild(PersonalCard);

                    // navigator.vibrate([200, 100, 200])
                } else if (req.status == 'DE') {
                    req.gate_out === "FE"
                        ? PersonalCard.classList.add("text-bg-dark")
                        : PersonalCard.classList.add("text-bg-secondary");
                    deliveredContainer.appendChild(PersonalCard);
                }
            });
            // Badges
            badge1.textContent = deliverRequestsContainer.children.length
            badge2.textContent = sentContainer.children.length
            badge3.textContent = deliveredContainer.children.length

            // Filter by search
            filterCards("search_input", document.getElementsByClassName("card"))
        }
    });
}
