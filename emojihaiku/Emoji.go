package emojihaiku

type Emoji struct {
	Emoji        string   `json:"emoji"`
	Descriptions []string `json:"descriptions"`
	Tags         []string `json:"tags"`
	Year         int      `json:"year"`
	DispMode     string   `json:"disp_mode"`
}
