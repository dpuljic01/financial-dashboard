<template>
  <div class="container">
    <h1>Courses</h1>
    <hr />
    <md-button class="md-raised" :md-ripple="false">Add course</md-button>
    <table class="table table-hover">
      <tr>
        <th scope="col">Title</th>
        <th scope="col">Author</th>
        <th scope="col">Paperback</th>
      </tr>
      <tbody>
        <tr v-for="(course, index) in courses" :key="index">
          <td>{{ course.title }}</td>
          <td>{{ course.author }}</td>
          <td>
            <span v-if="course.paperback">Yes</span>
            <span v-else>No</span>
          </td>
          <td>
            <md-button class="md-raised md-primary" :md-ripple="false">Update</md-button>
            <md-button class="md-raised md-accent" :md-ripple="false">Delete</md-button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Vue from 'vue';
import axios from 'axios';

export default {
  name: 'courses',
  data() {
    return {
      courses: [],
    };
  },
  methods: {
    getCourses() {
      const path = 'http://192.168.5.18:5000/api/courses';
      axios
        .get(path)
        .then((res) => {
          this.courses = res.data.courses;
        })
        .catch((error) => {
          Vue.$toast.open({
            message: error,
            type: 'error',
            duration: 3000,
          });
        });
    },
  },
  created() {
    this.getCourses();
  },
};
</script>
