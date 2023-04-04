function goBack() {
    if (window.history.length > 2) {
      window.history.go(-2);
    } else {
      window.history.back();
    }
  }
  
  const likeButtons = document.querySelectorAll('.like-button');
  const dislikeButtons = document.querySelectorAll('.dislike-button');
  
  likeButtons.forEach(button => {
    button.addEventListener('click', () => {
      const postId = button.dataset.postId;
      const isLiked = button.dataset.liked === 'true';
      const isDisliked = button.nextElementSibling.dataset.disliked === 'true';
  
      if (!isLiked) {
        button.dataset.liked = 'true';
        button.classList.add('liked');
        button.nextElementSibling.textContent = parseInt(button.nextElementSibling.textContent) + 1;
  
        if (isDisliked) {
          dislikeButtons.forEach(dislikeButton => {
            if (dislikeButton.dataset.postId === postId) {
              dislikeButton.dataset.disliked = 'false';
              dislikeButton.classList.remove('disliked');
              dislikeButton.nextElementSibling.textContent = parseInt(dislikeButton.nextElementSibling.textContent) - 1;
            }
          });
        }
      } else {
        button.dataset.liked = 'false';
        button.classList.remove('liked');
        button.nextElementSibling.textContent = parseInt(button.nextElementSibling.textContent) - 1;
      }
    });
  });
  
  dislikeButtons.forEach(button => {
    button.addEventListener('click', () => {
      const postId = button.dataset.postId;
      const isDisliked = button.dataset.disliked === 'true';
      const isLiked = button.previousElementSibling.dataset.liked === 'true';
  
      if (!isDisliked) {
        button.dataset.disliked = 'true';
        button.classList.add('disliked');
        button.previousElementSibling.textContent = parseInt(button.previousElementSibling.textContent) - 1;
  
      if (isLiked) {
        button.dataset.isliked = 'true';
        button.classList.add('isliked');
        button.previousElementSibling.textContent = parseInt(button.previousElementSibling.textContent) + 1;
      }

