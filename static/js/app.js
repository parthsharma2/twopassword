function setRandomPassword() {
  const passwordInput = document.querySelector('#id_password');
  const url = '/passwords/generate';

  if (!passwordInput) {
    console.error('No password input found!');
    return;
  }

  fetch(url)
    .then(resp => resp.json())
    .then(data => passwordInput.value = data.password)
    .catch(err => console.error('An unexpected error occured:', err));
}
