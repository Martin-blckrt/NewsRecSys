function splitList(list) {
  const size = list.length;
  const quotient = Math.floor(size / 3);
  const remainder = size % 3;

  let firstPart = [],
      secondPart = [],
      thirdPart = [];

  if (remainder === 0) {
    firstPart = list.slice(0, quotient);
    secondPart = list.slice(quotient, quotient * 2);
    thirdPart = list.slice(quotient * 2);
  } else if (remainder === 1) {
    firstPart = list.slice(0, quotient + 1);
    secondPart = list.slice(quotient + 1, quotient * 2 + 1);
    thirdPart = list.slice(quotient * 2 + 1);
  } else {
    firstPart = list.slice(0, quotient + 1);
    secondPart = list.slice(quotient + 1, quotient * 2 + 2);
    thirdPart = list.slice(quotient * 2 + 2);
  }

  return [firstPart, secondPart, thirdPart];
}

function shuffleList(list) {
  list.sort(() => Math.random() - 0.5);
  return list;
}

window.addEventListener("blur", () => {
  setTimeout(() => {
    if (document.activeElement.tagName === "IFRAME") {
      if (document.activeElement.title === 'Twitter Tweet') {
        console.log(document.activeElement.parentElement.parentElement.id);
        get_user_response(document.activeElement.parentElement.parentElement.id);
      } else {
        console.log(document.activeElement.parentElement.parentElement.parentElement.id);
        get_user_response(document.activeElement.parentElement.parentElement.parentElement.id);
      }
      window.focus();
    }
  });
});

var form = document.getElementById("my-form");
document.getElementById("submit-id").onclick = submit_id;

form.addEventListener("submit", function(event) {
  event.preventDefault(); // prevent the page from reloading
  showCards(); // call the showCards function to display the cards
});

function submit_id(event) {
  let user_id = document.getElementById("user-id").value;
  recommend_news(user_id);
  event.preventDefault();
}

function recommend_news(user_id) {
  let api_url = `http://127.0.0.1:8000/recommend-news/${user_id}`; // localhost-http
  // fetch url and make a get request
  fetch(api_url)
    .then(response => response.json())
    .then(data => {
      // data will contain the recommended news as an array of objects
      // you can access the news items like this:
      data = JSON.parse(data);
      console.log(data);

      for (var i = 0; i < data.length; i++) {
        var newsItem = data[i];
        if (newsItem.source !== 'twitter') {
          if (newsItem.source !== 'Futurology' && newsItem.source !== 'Technology' && newsItem.source !== 'Realtech' && newsItem.source !== 'Tech') {
            data[i].source = 'classic';
          } else {
            data[i].source = 'reddit';
          }
        }
        }
      showCards(data);
    })
    .catch(error => console.error(error));
}

function get_user_response(url) {

  let api_url = 'http://127.0.0.1:8000/response/';

  // Create a JSON payload with the URL
  let payload = {
    url: url
  };

  fetch(api_url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(
    (res) => {
      // if request is okay return its json, otherwise display an error
      if (res.ok) {
        return res.json();
      }
    }
  )
}

function createCard(title, image, description, link, type) {
  var card = '';
  
  if (type === 'classic') {
    card =    '<div class="card card-blog">' +
                '<a href="' + link + '" target="_blank">' +
                  '<div class="card-image">' +
                    '<figure style="margin-bottom: 0">' +
                      '<img class="img" src="' + image + '" alt="">' +
                    '</figure>' +
                    '<div class="card-caption">' + title + '</div>' +
                    '<div class="ripple-cont"></div>' +
                  '</div>' +
                  '<div class="table">' +
                    '<h6 class="category text-info"><i class="fa fa-soundcloud"></i> Data Science</h6>' +
                    '<p class="card-description">' + description + '</p>' +
                  '</div>' +
                '</a>' +
              '</div>';
  } else if (type === 'twitter') {
    const id = link.split("/status/")[1];
    link_embed = 'https://twitter.com/x/status/' + id;
    card =    '<div class="card twitter-card" id=' + link +'>' +
                '<blockquote class="twitter-tweet">' +
                  '<a href="' + link_embed + '"></a>' +
                '</blockquote>' +
            '</div>';
  } else if (type === 'reddit') {
  card = `
    <div class="card" id="${link}">
      <blockquote class="reddit-card"><a href=${link}></a></blockquote>
      <script async src="https://embed.redditmedia.com/widgets/platform.js" charset="UTF-8"></script>
    </div>
  `;
}
  
  return card;
}


function showCards(news_model) {
  news_model = shuffleList(news_model);
  lists = splitList(news_model);
  console.log(lists);
  id_cols = ['1','2','3'];

  for (let i = 0; i < id_cols.length; i++) {
    sub_news = lists[i];
    cardHtml = '';

    for (let j = 0; j < sub_news.length; j++) {
      var newsItem = sub_news[j];
      cardHtml += createCard(newsItem.title, newsItem.image, newsItem.description, newsItem.url, newsItem.source);
    }
    var id_col = 'col' + id_cols[i];
    var cardContainer = document.getElementById(id_col);
    cardContainer.innerHTML = cardHtml;
  }

  twttr.widgets.load();
  addListeners();
}

function addListeners() {
  const cards = document.querySelectorAll('.card, .card-blog');

  cards.forEach(card => {
    card.addEventListener('click', event => {
      const clickedCard = event.target.closest('a');
      console.log(clickedCard.getAttribute('href'));
      get_user_response(clickedCard.getAttribute('href'));
    });
  });
  twttr.widgets.load();
}


