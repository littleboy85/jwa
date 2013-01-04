/**
 * @license Copyright (c) 2003-2012, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
  // Define changes to default configuration here. For example:
  // config.language = 'fr';
  // config.uiColor = '#AADC6E';
  config.toolbarGroups = [
    { name: 'document',	   groups: ['doctools'] },
    { name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
    { name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
    { name: 'links' },
    { name: 'insert' },
    '/',
    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
    { name: 'styles' },
    { name: 'colors' },
    '/',
    { name: 'paragraph',   groups: [ 'list', 'indent', 'align' ] },
    {name: 'tools'},
    {name: 'mode'},
    {name: 'about'}
  ];

  // Remove some buttons, provided by the standard plugins, which we don't
  // need to have in the Standard(s) toolbar.
  config.removeButtons = 'Subscript,Superscript,Preview,NewPage,Print';

};
