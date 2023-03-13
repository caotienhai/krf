/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'client/templates/client/*.html',
    'poscrm/templates/poscrm/*.html',
    'dashboard/templates/dashboard/*.html',
    'lead/templates/lead/*.html',
    'team/templates/team/*.html',
    'userprofile/templates/userprofile/*.html',
    'project/templates/project/*.html',
    'order/templates/order/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    /** require('@tailwindcss/forms'),  */
    require('tailwindcss-tables')(),

    // If pulled in manually...
    require('./plugins/tailwindcss-tables')(),
  ],
  
}
