import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageImageComponent } from './recv-message-image.component';

describe('RecvMessageImageComponent', () => {
  let component: RecvMessageImageComponent;
  let fixture: ComponentFixture<RecvMessageImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageImageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
