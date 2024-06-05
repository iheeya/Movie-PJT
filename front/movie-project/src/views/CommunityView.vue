<template>
  <!-- <h1>게시글 생성</h1> -->
  <!-- <div v-for="movie in store.movies" :key="movie.id"> -->
    <!-- <template v-if="movie.id == movieId">
      <p>pick : {{ movie.title }}</p>
    </template> -->

   <div class="card">
  <h2>게시글 작성</h2>
  <form @submit.prevent="createReview">
    <div class="form-group">
      <label for="title">한줄평:</label>
      <input type="text" id="title" v-model.trim="title" />
    </div>
    <div class="form-group">
      <label for="content">감상평:</label>
      <textarea id="content" v-model.trim="content"></textarea>
    </div>
    <input type="submit" value="작성하기" />
  </form>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import { useMovieStore } from "@/stores/counter";

onMounted(() => {
store.getMovies();
});

const store = useMovieStore();
const route = useRoute();
const router = useRouter();

//내가 생성산 게시글이 몇번 영화에 쓰였는지 저장 가능
const movieId = ref(route.params.movieId);

const title = ref(null);
const content = ref(null);

const createReview = function () {
axios({
  method: "post",
  url: `${store.API_URL}/reviews/`,
  data: {
    title: title.value,
    content: content.value,
    movie: movieId.value,
  },
  headers: {
    Authorization: `Token ${store.token}`,
  },
})
  .then(() => {
    router.push({ name: "moive-detail", params: { name: movieId } });
  })
  .catch((err) => console.log(err));
};
</script>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 400px;
  margin: 0 auto; /* Centers the card horizontally */
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  border-radius: 8px;
}
form {
  width: 100%;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

input[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type="submit"]:hover {
  background-color: #0056b3;
}
</style>
