let post = {
  title: "Good Fries!",
  author: "Maddie",
  feedback: "Fries good!",
  comments: [
    {
      body: "I agree",
      author: "Leila",
      station: "Grill"
    }
  ],
  // get comments() {
  //   return this.comments;
  // },
  // set comments(value) {
  //   this.comments = value;
  // },
  addComment: function() {
      let comment = prompt("Comment here:");
      if (comment) {
        this.comments.push(comment);
        this.displayComments();
      }
  },
  displayComments: function() {
      let list = document.getElementById("comments");
      list.innerHTML = "";
      for (let i = 0; i < this.comments.length; i++) {
          let item = document.createElement("li");
          item.textContent = this.comments(i);
          list.appendChild(item);

      }
  },
  likes: 5,
  shares: 2
}

document.getElementById("feedback").textContent=post.description,
post.displayComments();

function toggleMenu() {
  let menu = document.getElementById('menu');
  menu.classList.toggle('active');
};

document.addEventListener("click", function(event) {
  const dropdownMenu = document.querySelector(".cool ul#menu");
  const webpage = document.querySelector("togglemenu");

  if (!dropdownMenu.contains(event.target) && event.target !== webpage) {
    dropdownMenu.classList.remove("show");
  }
});
