<template>
  <div>
    <!-- <h1>리뷰 디테일</h1> -->
    <!-- {{ reviewId }} -->
    <section class="review-section">
      <div v-for="review in store.reviews">
        <div v-for="movie in store.movies">
          <template v-if="review.id == reviewId && review.movie == movie.id">
            <div class="row justify-content-around">
              <div class="col-4">
                <RouterLink
                  :to="{
                    name: 'ProfileView',
                    params: { username: review.user },
                  }"
                  class="custom-link"
                  style="font-size: 20px"
                >
                  {{ review.user }}
                </RouterLink>

                <p>{{ movie.title }}</p>
                <p>
                  <i class="fa-solid fa-star" style="color: yellow"></i>
                  {{ movie.vote_average.toFixed(1) }}
                </p>
                <p>한줄평: {{ review.title }}</p>
                <p>감상평: {{ review.content }}</p>
              </div>
              <div class="col-4">
                <p style="text-align: right">
                  <RouterLink
                    :to="{
                      name: 'moive-detail',
                      params: { movieId: movie.id },
                    }"
                  >
                    <img
                      :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`"
                      alt="Movie Poster"
                    />
                  </RouterLink>
                </p>
              </div>
            </div>
            <!-- 모달 구현 -->
            <!-- <form @submit.prevent="createComment">
            <input
              class="form-control"
              type="text"
              id="comment"
              v-model.trim="comment"
              placeholder="댓글을 입력해주세요."
            />
            <input type="submit">
          </form> -->
            <div class="review-btn">
              <!-- 댓글작성 버튼 -->
              <div class="row justify-content-around">
                <div class="col-4">
                  <button
                    @click="showModal = true"
                    class="btn"
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModal"
                    v-if="store.isLogin"
                  >
                    <i
                      class="fa-regular fa-message"
                      style="color: #6d4eca; font-size: 30px"
                    ></i>
                  </button>
                  <!-- 삭제 버튼 -->
                  <template v-if="review.user == store.name">
                    <button @click="deleteReview(review, movie)" class="btn">
                      <i
                        class="fa-regular fa-trash-can"
                        style="color: #d41111; font-size: 30px"
                      ></i>
                    </button>
                  </template>
                </div>
                <div class="col-4"></div>
              </div>

              <!-- 모달 -->
              <div
                class="modal fade"
                id="exampleModal"
                tabindex="-1"
                aria-labelledby="exampleModalLabel"
                aria-hidden="true"
              >
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                    <div class="modal-header" style="border-bottom: none">
                      <h5 class="modal-title" style="color: black">댓글</h5>
                      <button
                        type="button"
                        class="btn-close"
                        aria-label="Close"
                        @click="closeModal"
                      ></button>
                    </div>
                    <div class="modal-body">
                      <form @submit.prevent="createComment">
                        <div class="mb-3">
                          <textarea
                            id="comment"
                            v-model.trim="comment"
                            class="form-control"
                            style="width: 100%; height: 150px; border: none"
                            placeholder="댓글을 입력하세요."
                          ></textarea>
                        </div>
                        <div class="mb-3 text-center">
                          <input
                            type="submit"
                            value="작성하기"
                            class="btn btn-secondary"
                          />
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>

      <CommentList />
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, RouterLink, useRouter } from "vue-router";
import { useMovieStore } from "@/stores/counter";
import CommentList from "@/components/CommentList.vue";
import axios from "axios";

const route = useRoute();
//내가 생성한 게시글이 몇번 영화에 쓰였는지 저장 가능
const reviewId = ref(route.params.reviewId);
const comment = ref(null);
const store = useMovieStore();
// console.log(reviewId.value)
// console.log(store.token)
const router = useRouter();

const showModal = ref(false);

const closeModal = () => {
  showModal.value = false;
  const myModalEl = document.getElementById("exampleModal");
  const modal = bootstrap.Modal.getInstance(myModalEl);
  modal.hide();
};

const createComment = function () {
  if (!comment.value) {
    alert("내용을 입력해주세요.");
    return;
  }

  axios({
    method: "post",
    url: `${store.API_URL}/comments/create/`,
    data: {
      comment: comment.value,
      review: reviewId.value,
    },
    headers: {
      Authorization: `Token ${store.token}`,
      "Content-Type": "application/json",
    },
  })
    .then(() => {
      closeModal();
      store.getComments();
      // router.push({ name: "ReviewDetail", params:{reviewId:reviewId.value} });
      comment.value = null;
    })
    .catch((err) => console.log(err));
};

const deleteReview = function (review, movie) {
  axios({
    method: "DELETE",
    url: `${store.API_URL}/reviews/delete/${review.id}`,
  })
    .then((response) => {
      // console.log(response)
      // router.push({ name: "moive-detail", params: { name: movieId } });
      store.getReviews();
      store.reviews = store.reviews.filter((c) => c.id !== review.id);

      // 영화 디테일 페이지로 이동
      router.push(`/movie/${movie.id}`);
    })
    .catch((error) => {
      console.log(error);
    });
};
</script>

<style scoped>
.review-section {
  margin: 50px 100px;
}

.custom-link {
  text-decoration: none; /* 밑줄 제거 */
  color: white; /* 글씨 색 변경 (파란색) */
}
</style>
