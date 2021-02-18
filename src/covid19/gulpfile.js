"use strict";

// Load plugins
const browsersync = require("browser-sync").create();
const del = require("del");
const gulp = require("gulp");
const merge = require("merge-stream");

// BrowserSync
function browserSync(done) {
  browsersync.init({
    server: {
      baseDir: "./"
    },
    port: 3000
  });
  done();
}

// BrowserSync reload
function browserSyncReload(done) {
  browsersync.reload();
  done();
}

// Clean vendor
function clean() {
  return del(["./vendor/"]);
}

// Bring third party dependencies from node_modules into vendor directory
function modules() {
    var bootstrap = gulp.src('./node_modules/bootstrap/dist/**/*').pipe(gulp.dest('./static/vendor/bootstrap'));
    var jquery = gulp.src(['./node_modules/jquery/dist/*','!./node_modules/jquery/dist/core.js'])
        .pipe(gulp.dest('./static/vendor/jquery'));
    var popper_js = gulp.src(['./node_modules/popper.js/dist/**/*']).pipe(gulp.dest('./static/vendor/popper.js'));
    var fontawesome = gulp.src(['./node_modules/@fortawesome/fontawesome-free/**/*'])
        .pipe(gulp.dest('./static/vendor/fontawesome-free'));
    var bootswatch = gulp.src(['./node_modules/bootswatch/dist/**/*']).pipe(gulp.dest('./static/vendor/bootswatch'));
    return merge(
        bootstrap, jquery, popper_js, fontawesome, bootswatch
    );
}

// Watch files
function watchFiles() {
  gulp.watch("./**/*.css", browserSyncReload);
  gulp.watch("./**/*.html", browserSyncReload);
}

// Define complex tasks
const vendor = gulp.series(clean, modules);
const build = gulp.series(vendor);
const watch = gulp.series(build, gulp.parallel(watchFiles, browserSync));

// Export tasks
exports.clean = clean;
exports.vendor = vendor;
exports.build = build;
exports.watch = watch;
exports.default = build;
