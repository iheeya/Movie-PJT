<template>
  <div>
  <hr>
  <div class="review-container">
  <div>
      <div v-for="comment in store.comments">
        <template v-if="comment.review == reviewId">
          <div class="comment-container">
            <div>
              {{ comment.user }} : {{ comment.comment }}
            <span v-if="comment.user == store.name">
              <button @click="deleteComment(comment)" class="btn">
                <i class="fa-sharp fa-solid fa-xmark" style="color: red;"></i>
              </button>
            </span>
          </div>
          </div>
        <br>
        </template>
      </div>
  </div>
</div>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { useMovieStore } from "@/stores/counter";
import axios from 'axios'

const route = useRoute();
//내가 생성산 게시글이 몇번 영화에 쓰였는지 저장 가능
const reviewId = ref(route.params.reviewId);
const store = useMovieStore();
console.log(store.comments.id)

// 댓글 삭제 기능 함수
const deleteComment = function(comment){
  axios({
    method: 'DELETE', 
    url: `${store.API_URL}/comments/delete/${comment.id}`
  })
    .then((response)=>{
      console.log(response)
      store.getComments()
      store.comments = store.comments.filter(c => c.id !== comment.id);
    })
    .catch((error) =>{
      console.log(error)
    })
}


onMounted(() => {
  store.getComments(); // getComments 호출
});

console.log(store.comments)
</script>

<style  scoped>
.review-container {
  margin-left: 150px;
}

</style>






