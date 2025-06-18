<script setup lang="ts">
// import FileImporter from "./components/FileImporter.vue";
</script>

<template>
  <div>
    <nav id="navigation">
      <router-link to="/">Home</router-link>
      <router-link to="/file_import">Image Import</router-link>
    </nav>
  </div>

  <router-view />
<!--  <FileImporter />-->
</template>
<style scoped>
  #navigation {
    background:darkcyan;
    display:flex;
    flex-direction: row;
    gap:2rem;
    padding:1rem;
    border-radius:5px;
    margin-bottom:2rem;
    width:40rem;
    height:auto;
  }

  a {
    color:white;
    background:transparent;
  }

  a:hover {
    text-shadow: whitesmoke 0px 5px 15px;
    color:navajowhite;
  }

</style>
