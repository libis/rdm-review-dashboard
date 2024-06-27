
export interface NoteTag {
    type: string | null;
    content: string;
}


export interface Note {
    version: string | null;
    userId: string;
    noteId: string;
    created: Date;
    persistentId: string;
    noteType: string;
    text: string;
    modified: Date;
    tags: NoteTag[];
}

export interface HistoryItem {
    userId: string;
    created: Date;
    text: string;
    category: string;
    subcategory: string;
}

