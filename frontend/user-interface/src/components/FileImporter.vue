<script setup lang="ts">
  import {ref} from 'vue'

  // ------- some important endpoints info ------
  const imageEndpoint = "/api/uploads/images";
  const host = "http://localhost:8000"
  let fileToBeUploaded: undefined | File = undefined;


  const imagePreview = ref<string>('');
  const imageInput = ref<HTMLInputElement | null>(null);
  const firstNameInput = ref<HTMLInputElement | null>(null)
  const lastNameInput = ref<HTMLInputElement | null>(null)


  function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (file) {
      fileToBeUploaded = file;
      const reader = new FileReader();
      reader.onload = (e) => {  // registers the callback
        imagePreview.value = e.target?.result as string;
      };
      reader.readAsDataURL(file);  // this function actually triggers the onload, it's asynchronous
    }
  }

  function triggerFileUpload() {
    imageInput.value?.click();
  }

  function triggerBackendUpload() {
      if (!firstNameInput.value?.value) {
        window.alert("You must input the first name!")
        return
      }
      if (!lastNameInput.value?.value) {
        window.alert("You must input the last name!")
        return
      }

      if (!fileToBeUploaded) {
        window.alert("You must select an Image first!")
        return;
      }

      // upload to API
      const formData = new FormData();
      formData.append('imgUpload', fileToBeUploaded);
      formData.append("firstName", firstNameInput.value.value)
      formData.append('lastName', lastNameInput.value.value)

      fetch(`${host}${imageEndpoint}`, {
        method: "POST",
        body: formData
      })
          .then(res => res.json())
          .then(data => {
            console.log("Response from backend: ", data)
          })
          .catch(err => console.log("Error uploading image: ", err))
  }

  function clearInput() {
    imageInput.value = null;
    imagePreview.value ='';
    fileToBeUploaded = undefined;
  }

</script>

<template>
  <div>
    <h2>File Import Panel</h2>
    <input
      type= "file"
      ref = "imageInput"
      @change ="handleFileUpload"
      accept = "image/*"
      style="display:none"
      />
    <button id="select-btn" @click = "triggerFileUpload">Select Image</button>

    <div id="image-preview-container">
      <h3>Image Preview</h3>
      <img v-if ="imagePreview" id="image-previewer" :src="imagePreview" alt="preview-image" />

      <div class="input-container">
        <label>First Name:</label>
        <input
            ref = "firstNameInput"
            type="text"
            style="display:inline-block"
            required
        />
      </div>

      <div class="input-container">
        <label>Last Name:</label>
        <input
            ref ="lastNameInput"
            type="text"
            style="display:inline-block"
            required
          />
      </div>

      <button id="upload-btn" @click="triggerBackendUpload" >Upload</button>
      <button id="clear-input-btn" @click="clearInput">Clear</button>

    </div>
  </div>

</template>

<style scoped>
  *{
    margin:0; padding:0;
  }

  #upload-btn {
    margin:1rem;
    background:orange;
    padding:0.5rem;
    width:10rem;
    display:inline-block;
  }

  #upload-btn:hover{
    background: #dc6606;
  }

  #clear-input-btn {
    margin:1rem;
    background: #f46969;
    padding:0.5rem;
    width:10rem;
    display:inline-block;
  }

  #clear-input-btn:hover{
    background:tomato;
  }

  #select-btn {
    margin:1rem;
    background:green;
    padding:0.8rem;
    width:10rem;
  }

  #select-btn:hover{
    background: #2b682b;
  }

  #image-previewer {
    width:300px;
    height:300px;
    display:block;
    justify-self: center;
  }

  .input-container{
    padding:1rem;
    display:block;
  }

  .input-container label {
    margin-right: 1rem;
  }

  .input-container input {
    padding:5px;
    font-size:1rem;
    border-radius: 5px;
  }

  .input-container input:focus {
    border: 2px solid dodgerblue;
    outline:none;
  }

  #image-preview-container {
    margin:1rem;
    padding:2rem;
    border-radius: 5px;
    box-shadow: rgba(0, 0, 0, 0.24) 0 3px 8px;
  }
</style>