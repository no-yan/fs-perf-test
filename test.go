package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sync"
	"time"
)

func walk(path string) error {
	return filepath.Walk(path, func(path string, info os.FileInfo, err error) error {
		return nil // or add actual processing here
	})
}

func main() {
	var (
		jobs  = flag.Int("j", runtime.NumCPU(), "Number of parallel processes")
		limit = flag.Int("l", 100, "Number of walks to execute")
	)

	flag.Parse()

	if flag.NArg() != 1 {
		fmt.Println("Usage: test [options] <path>")
		os.Exit(1)
	}

	path := flag.Arg(0)

	sem := make(chan struct{}, *jobs)
	start := time.Now()
	var wg sync.WaitGroup

	for i := 0; i < *limit; i++ {
		wg.Add(1)

		go func() {
			defer wg.Done()
			sem <- struct{}{}
			if err := walk(path); err != nil {
				fmt.Printf("Error during walk: %v\n", err)
			}
			<-sem
		}()
	}

	wg.Wait()
	elapsed := time.Since(start)

	fmt.Printf("Ran %d walks across %d processes in %.3fs\n", *limit, *jobs, elapsed.Seconds())
}
