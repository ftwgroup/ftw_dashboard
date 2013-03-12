<div class="googledrive">
    {{#if authenticated}}
        <div>
            <span class="googledrive-refresh">Refresh</span> -
            <span class="googledrive-close">Close</span>
        </div>
        {{#each files}}
            <div class="googledrive-file">
                <a class="googledrive-file-import" href="javascript: void(0);" data-docid="{{this.id}}">Import</a> -
                <a class="googledrive-file-edit" href="{{this.alternateLink}}" target="_blank" title="Open this document in a separate window">{{this.title}}</a>
            </div>
        {{else}}
            <div>Your Google Drive files will be listed here.</div>
        {{/each}}
    {{else}}
        <div>
            <span class="googledrive-close">Close</span>
        </div>
        <a class="googledrive-login" href="javascript: void(0);">Login to Google Drive</a>
    {{/if}}
</div>
