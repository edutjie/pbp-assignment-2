# Assignments 5: Web Design Using HTML, CSS, and CSS Framework

**Nama:** Eduardus Tjitrahardja

**NPM:** 2106653602

**Kelas:** D

**Link:** [Deployed Heroku Website](https://edutjie-pbp-2.herokuapp.com/todolist/)

## Difference between Inline, Internal, dan External CSS?
**Internal CSS** requires you to add `<style>` tag in the `<head>` section of your HTML document. **Internal CSS** is an effective method of styling a single page. However, using this style for multiple pages is time-consuming as you need to put CSS rules on every page of your website. With **External CSS**, you’ll link your web pages to an external .css file. **External CSS** is a more efficient method, especially for styling a large website. By editing one .css file, you can change your entire site at once. **Inline CSS** is used to style a specific HTML element. For this CSS style, you’ll only need to add the style attribute to each HTML tag, without using selectors. **Inline CSS** is not really recommended if you want to style many pages at onces, as each HTML tag needs to be styled individually but it is very effective if you only want to style just 1 element. 

## HTML Tags
- `<div>`
  - defines a division or a section in an HTML document.
- `<a>`
  - defines a hyperlink, which is used to link from one page to another.
- `<p>`
  - defines a paragraph.
- `<table>`
  - defines an HTML table.
  - consists of `<tr>` (row), `<th>` (header cell), and `<td>` (data cell)
- `<input>`
  - specifies an input field where the user can enter data.
- etc


## CSS Selectors
- `*` : Selects all elements
- `.example` : Selects all elements with `class="example"`
- `#example` : 	Selects the element with `id="example"
- `example` : Selects all `<example>` elements
- `example:hover` : Selects all elements with `class="example"` on mouse over
- etc   

## This assignment implementation
I used tailwind css framework for this assignment because it makes styling easier since we just have to add classes that are implemented by tailwind in the element's class. For more information about the classes visi https://tailwindcss.com/. Before we can use tailwind's classes, we have to add `<script src="https://cdn.tailwindcss.com"></script>` in our `base.html` header.

After I have implemented all styling to the pages, I made it responsive using the media queries breakpoint from tailwind (`sm:`, `md:`, `lg:`, `xl:`, and `2xl:`) infront of the classes. For example, `flex-col md:flex-row` to make it `flex-row` when the our website width reaches the `md:` breakpoint and `flex-col` for anything below the md breakpoint. For more information of the breakpoints, visit https://tailwindcss.com/docs/responsive-design.